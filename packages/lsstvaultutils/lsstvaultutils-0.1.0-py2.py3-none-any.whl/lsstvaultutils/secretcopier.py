#!/usr/bin/env python
"""SecretCopier aids migration between Vault and Kubernetes secrets.
"""

import click
import hvac
from base64 import b64decode, b64encode
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from .timeformatter import getLogger


@click.command()
@click.argument("k8s_secret_name")
@click.argument("vault_secret_path")
@click.option("--url", envvar="VAULT_ADDR", help="URL of Vault endpoint.")
@click.option("--token", envvar="VAULT_TOKEN", help="Vault token to use.")
@click.option(
    "--cacert", envvar="VAULT_CAPATH", help="Path to Vault CA certificate."
)
@click.option(
    "--debug", envvar="DEBUG", is_flag=True, help="Enable debugging."
)
def standalonek2v(
    url, token, cacert, k8s_secret_name, vault_secret_path, debug
):
    """Copy from Kubernetes to Vault."""
    client = SecretCopier(url, token, cacert, debug)
    client.copy_k8s_to_vault(k8s_secret_name, vault_secret_path)


@click.command()
@click.argument("vault_secret_path")
@click.argument("k8s_secret_name")
@click.option("--url", envvar="VAULT_ADDR", help="URL of Vault endpoint.")
@click.option("--token", envvar="VAULT_TOKEN", help="Vault token to use.")
@click.option(
    "--cacert", envvar="VAULT_CAPATH", help="Path to Vault CA certificate."
)
@click.option(
    "--debug", envvar="DEBUG", is_flag=True, help="Enable debugging."
)
def standalonev2k(
    url, token, cacert, k8s_secret_name, vault_secret_path, debug
):
    """Copy from Vault to Kubernetes."""
    client = SecretCopier(url, token, cacert, debug)
    client.copy_vault_to_k8s(vault_secret_path, k8s_secret_name)


class SecretCopier(object):
    """Class to copy secrets between Kubernetes and Vault."""

    def __init__(self, url, token, cacert, debug=False):
        self.logger = getLogger(name=__name__, debug=debug)
        self.logger.debug("Debug logging started.")
        if not url and token and cacert:
            raise ValueError(
                "All of Vault URL, Vault Token, and Vault CA "
                + "path must be present, either in the "
                + "or as options."
            )
        self.vault_client = self.get_vault_client(url, token, cacert)
        self.k8s_client = self.get_k8s_client()
        self.current_context = config.list_kube_config_contexts()[1]
        self.namespace = self.current_context["context"]["namespace"]
        self.secret = {}

    def canonicalize_secret_path(self, path):
        if path[:7].lower() == "secret/":
            self.logger.debug("Removing 'secret/' from front of path.")
            path = path[7:]
        return path

    def get_vault_client(self, url, token, cacert):
        """Acquire a Vault client."""
        self.logger.debug("Acquiring Vault client for '%s'." % url)
        client = hvac.Client(url=url, token=token, verify=cacert)
        assert client.is_authenticated()
        return client

    def get_k8s_client(self):
        """Acquire a Kubernetes client from currently-selected config."""
        self.logger.debug("Acquiring k8s client.")
        config.load_kube_config()
        k8s_client = client.CoreV1Api()
        return k8s_client

    def encode_secret_data(self):
        """Base64-encode secret data for Kubernetes storage."""
        self.logger.debug("Base64-encoding secret data")
        self.encoded_secret = {}
        for k in self.secret:
            self.encoded_secret[k] = b64encode(
                self.secret[k].encode("utf-8")
            ).decode("utf-8")

    def read_k8s_secret(self, k8s_secret_name):
        """Read a secret from Kubernetes."""
        self.logger.debug(
            "Reading secret from '%s' " % k8s_secret_name
            + " in namespace '%s'." % self.namespace
        )
        secret = self.k8s_client.read_namespaced_secret(
            k8s_secret_name, self.namespace
        )
        data = secret.data
        self.encoded_secret = data
        self.secret = {}
        for k in data:
            v = data[k]
            if v:
                self.secret[k] = b64decode(v).decode("utf-8")
            else:
                self.secret[k] = v

    def write_vault_secret(self, vault_secret_path):
        """Write a secret to Vault."""
        self.logger.debug("Writing secret to '%s'." % vault_secret_path)
        for k in self.secret:
            spath = vault_secret_path + "/" + k
            self.logger.debug("Writing secret to '%s'." % spath)
            self.vault_client.secrets.kv.v2.create_or_update_secret(
                spath, secret={"value": self.secret[k]}
            )

    def copy_k8s_to_vault(self, k8s_secret_name, vault_secret_path):
        """Copy secret from Kubernetes to Vault."""
        vault_secret_path = self.canonicalize_secret_path(vault_secret_path)
        self.read_k8s_secret(k8s_secret_name)
        self.write_vault_secret(vault_secret_path)

    def read_vault_secret(self, vault_secret_path):
        """Read a secret from Vault."""
        self.logger.debug("Reading secret from '%s'." % vault_secret_path)
        path = vault_secret_path
        pathcomps = path.split("/")
        basepath = "/".join(pathcomps[:-1])
        lastcomp = pathcomps[-1]
        v2c = self.vault_client.secrets.kv.v2
        vkeys = v2c.list_secrets(basepath)["data"]["keys"]
        valdata = {}
        if lastcomp in vkeys:
            # It will end with a "/" if it's a directory, but not if
            #  it is a simple value
            self.logger.debug("'%s' is a single value." % vault_secret_path)
            value = v2c.read_secret_version(["data"]["data"]["value"])
            valdata = {lastcomp: value}
        elif (lastcomp + "/") in vkeys:
            self.logger.debug("'%s' is a set of values." % vault_secret_path)
            vkeys = v2c.list_secrets(vault_secret_path)["data"]["keys"]
            for k in vkeys:
                valdata[k] = v2c.read_secret_version(
                    vault_secret_path + "/" + k
                )["data"]["data"]["value"]
        self.secret = valdata

    def write_k8s_secret(self, k8s_secret_name):
        """Write a secret to Kubernetes."""
        oldsecret = None
        self.logger.debug(
            "Determining whether secret '%s'" % k8s_secret_name
            + "exists in namespace '%s'." % self.namespace
        )
        # If the secret already exists, we patch it.  Otherwise, we create it.
        try:
            oldsecret = self.k8s_client.read_namespaced_secret(
                k8s_secret_name, self.namespace
            )
            self.logger.debug("Secret found.")
        except ApiException as exc:
            if exc.status != 404:
                raise
            self.logger.debug("Secret not found.")
        self.encode_secret_data()
        secret = None
        if oldsecret:
            secret = oldsecret
            secret.data.update(self.encoded_secret)
        else:
            secret = client.V1Secret()
            secret.metadata = client.V1ObjectMeta()
            secret.metadata.name = k8s_secret_name
            secret.metadata.namespace = self.namespace
            secret.data = self.encoded_secret
        if oldsecret:
            self.logger.debug("Updating secret.")
            self.k8s_client.patch_namespaced_secret(
                k8s_secret_name, self.namespace, secret
            )
        else:
            self.logger.debug("Creating secret.")
            self.k8s_client.create_namespaced_secret(self.namespace, secret)

    def copy_vault_to_k8s(self, vault_secret_path, k8s_secret_name):
        """Copy a secret from Vault to Kubernetes."""
        vault_secret_path = self.canonicalize_secret_path(vault_secret_path)
        self.read_vault_secret(vault_secret_path)
        self.write_k8s_secret(k8s_secret_name)


if __name__ == "__main__":
    standalonek2v()
