# MyYoloTestBed

## Development Environment Setup
<details>
<summary>Installation</summary>
Installation via conda with requirement.txt

Ubuntu

```shell
$ while read requirement; do conda install --yes $requirement || pip install $requirement; done < requirements.txt
```

 Window
```shell
FOR /F "delims=~" %f in (requirements.txt) DO conda install --yes "%f"
```

</details>


## Yolov5

<details>
<summary>Yolov5</summary>
#### Convert CCPD data set to Yolo format
Command: 

``` shell
python CCPD2Yolo.py --data .\datasets\CCPD\images\train_ccpd_base  --output .\datasets\CCPD\labels\train_ccpd_base
python CCPD2Yolo.py --data .\datasets\CCPD\images\val_ccpd_base    --output .\datasets\CCPD\labels\val_ccpd_base
python CCPD2Yolo.py --data .\datasets\CCPD\images\test_ccpd_base   --output .\datasets\CCPD\labels\test_ccpd_base
```



Train customer data

``` shell 
python train.py --img 1088 --rect --batch 64 --epochs 6 --data ccpd_ds.yaml --weights yolov5s.pt
```



#### Inference
```shell
python detect.py --weights last.pt --img 1024 --conf 0.25 --source data/images/ --save-crop
```



#### Export
```shell
python export.py --weights yolov5s.pt  --batch 1 --include torchscript --optimize --inplace
```

</details>


## YOLOX
https://github.com/Megvii-BaseDetection/YOLOX

convert the CCPD data to coco format
https://github.com/weidafeng/CCPD2COCO
