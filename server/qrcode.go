package server

import (
	"bytes"
	"encoding/base64"
	"image/png"
	"net/url"
	"strings"

	"github.com/pquerna/otp"
	"github.com/spf13/viper"
	"github.com/ubccr/mokey/ipa"
)

func QRCode(otptoken *ipa.OTPToken, realm string) (string, error) {
	if otptoken == nil {
		return "", nil
	}

	uri := otptoken.URI
	customIssuer := viper.GetString("accounts.otp_issuer")
	if customIssuer != "" {
		ipaUrl, err := url.Parse(otptoken.URI)
		if err != nil {
			return "", err
		}
		v := ipaUrl.Query()
		v.Set("issuer", customIssuer)
		u := url.URL{
			Scheme:   "otpauth",
			Host:     strings.ToLower(otptoken.Type),
			Path:     "/" + customIssuer + ":" + otptoken.DisplayName(),
			RawQuery: v.Encode(),
		}

		uri = u.String()
	}

	key, err := otp.NewKeyFromURL(uri)
	if err != nil {
		return "", err
	}

	var buf bytes.Buffer
	img, err := key.Image(250, 250)
	if err != nil {
		return "", err
	}

	png.Encode(&buf, img)
	return base64.StdEncoding.EncodeToString(buf.Bytes()), nil
}
