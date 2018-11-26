# PmodGyro
This code was written for raspberry Pi pmod hat created by Design Spark (https://github.com/DesignSparkrs/DesignSpark.Pmod). The code was developed for PmodGyro

```
cd ~
git clone https://github.com/lbaitemple/PmodGyro/
cd ~/PmodGyro
sudo cp Gyro.py /usr/local/lib/python2.7/dist-packages/DesignSpark/Pmod
sudo mv /usr/local/lib/python2.7/dist-packages/DesignSpark/Pmod/HAT.py /usr/local/lib/python2.7/dist-packages/DesignSpark/Pmod/HAT.py.orig
python runGyro.py
```
