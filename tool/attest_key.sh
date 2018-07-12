#!/bin/bash
if [ ! -n "$1" ]; then
	echo "please input keyfile\n"
	exit
fi

if [ ! -n "$2" ]; then
	python attest_cut_key.py --in=$1
else
	python attest_cut_key.py --in=$1 --skip=$2
fi

if [ "$?" != 0 ]; then
	echo "key cut fail\n"
	exit
fi

midfile1="AttestCert.rsa0 AttestCert.rsa1 AttestCert.rsa2 AttestKey.rsa"
midfile2="AttestCert.ec0 AttestCert.ec1 AttestCert.ec2 AttestKey.ec"

cd provisionkey
for file in `ls *.origin`
do
	../attest_parse_key.py --in $file
	openssl rsa -inform PEM -in AttestKey.rsa.pem -outform DER -out AttestKey.rsa
	openssl ec -inform PEM -in AttestKey.ec.pem -outform DER -out AttestKey.ec
	openssl x509 -inform PEM -in AttestCert.rsa0.pem -outform DER -out AttestCert.rsa0
	openssl x509 -inform PEM -in AttestCert.rsa1.pem -outform DER -out AttestCert.rsa1
	openssl x509 -inform PEM -in AttestCert.rsa2.pem -outform DER -out AttestCert.rsa2
	openssl x509 -inform PEM -in AttestCert.ec0.pem -outform DER -out AttestCert.ec0
	openssl x509 -inform PEM -in AttestCert.ec1.pem -outform DER -out AttestCert.ec1
	openssl x509 -inform PEM -in AttestCert.ec2.pem -outform DER -out AttestCert.ec2
	../attest_pack_key.py --in ${file%.*}
	cp ../unifykey/${file%.*}.keybox ./ -f
	../provision_keywrapper -i ${file%.*}.keybox -t 0x42
	rm -rf *.pem
	rm -rf ${file%.*}.keybox
	rm -rf $file
	rm -rf ${midfile1} ${midfile2}
done
cd ..
