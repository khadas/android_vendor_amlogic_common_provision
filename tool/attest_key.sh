#!/bin/bash
if [ ! -n "$1" ]; then
echo "please input keyfile\n"
exit
fi

python attest_cut_key.py --in=$1

if [ "$?" != 0 ]; then
echo "key cut fail\n"
exit
fi

midfile1="AttestCert.rsa0 AttestCert.rsa1 AttestCert.rsa2 AttestKey.rsa"
midfile2="AttestCert.ec0 AttestCert.ec1 AttestCert.ec2 AttestKey.ec"

cd provisionkey
for dir in `ls .`
do
	if [ -d $dir ]
	then
		cd $dir
		openssl rsa -inform PEM -in AttestKey.rsa.pem -outform DER -out AttestKey.rsa
		openssl ec -inform PEM -in AttestKey.ec.pem -outform DER -out AttestKey.ec
		openssl x509 -inform PEM -in AttestCert.rsa0.pem -outform DER -out AttestCert.rsa0
		openssl x509 -inform PEM -in AttestCert.rsa1.pem -outform DER -out AttestCert.rsa1
		openssl x509 -inform PEM -in AttestCert.rsa2.pem -outform DER -out AttestCert.rsa2
		openssl x509 -inform PEM -in AttestCert.ec0.pem -outform DER -out AttestCert.ec0
		openssl x509 -inform PEM -in AttestCert.ec1.pem -outform DER -out AttestCert.ec1
		openssl x509 -inform PEM -in AttestCert.ec2.pem -outform DER -out AttestCert.ec2
		../../provision_keywrapper -i AttestCert.ec0
		../../provision_keywrapper -i AttestCert.ec1
		../../provision_keywrapper -i AttestCert.ec2
		../../provision_keywrapper -i AttestKey.ec
		../../provision_keywrapper -i AttestCert.rsa0
		../../provision_keywrapper -i AttestCert.rsa1
		../../provision_keywrapper -i AttestCert.rsa2
		../../provision_keywrapper -i AttestKey.rsa
		../../attest_pack_key.py --in $dir
		rm -rf *.pem
		rm -rf ${midfile1} ${midfile2}
		cd ..
	fi
done
cd ..
