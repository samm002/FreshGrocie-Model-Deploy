import base64
import hashlib
import hmac
import random
import requests
import string
import time
import urllib.parse


class FatSecretClient:
    def __init__(self, consumer_key, consumer_secret, base_url):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.base_url = base_url

    def generate_nonce(self, length=10):
        """Generate a random nonce string."""
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    def create_signature_base_string(self, method, params):
        """Create the signature base string as per FatSecret documentation."""
        # Sort parameters alphabetically
        sorted_params = sorted(params.items(), key=lambda x: (x[0], x[1]))

        # Create normalized parameter string
        param_string = "&".join(
            f"{urllib.parse.quote(str(k))}={urllib.parse.quote(str(v))}"
            for k, v in sorted_params
        )

        # Create signature base string
        signature_base = "&".join(
            [
                method.upper(),
                urllib.parse.quote(self.base_url, safe=""),
                urllib.parse.quote(param_string, safe=""),
            ]
        )

        return signature_base

    def generate_signature(self, signature_base_string, access_secret=""):
        """Generate HMAC-SHA1 signature."""
        # Create key by combining consumer secret and access secret with &
        key = f"{urllib.parse.quote(self.consumer_secret, safe='')}&{access_secret}"

        # Generate signature using HMAC-SHA1
        raw_hmac = hmac.new(
            key.encode("utf-8"), signature_base_string.encode("utf-8"), hashlib.sha1
        ).digest()

        # Base64 encode the HMAC value
        signature = base64.b64encode(raw_hmac).decode("utf-8")

        return signature

    def make_request(
        self, method="GET", api_method="foods.search", **additional_params
    ):
        """Make a request to the FatSecret API."""
        # Prepare OAuth parameters
        oauth_params = {
            "oauth_consumer_key": self.consumer_key,
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": str(int(time.time())),
            "oauth_nonce": self.generate_nonce(),
            "oauth_version": "1.0",
            "method": api_method,
            "format": "json",
        }

        # Add additional parameters
        params = {**oauth_params, **additional_params}

        # Generate signature base string
        signature_base_string = self.create_signature_base_string(method, params)

        # Generate signature
        signature = self.generate_signature(signature_base_string)

        # Add signature to parameters
        params["oauth_signature"] = signature

        # Make the request
        if method.upper() == "POST":
            response = requests.post(self.base_url, data=params)
        else:
            response = requests.get(self.base_url, params=params)

        return response.json()
