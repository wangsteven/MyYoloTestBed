# MyYoloTestBed
My Yolo Testbed

# Convert CCPD data set to Yolo format
command: 

python CCPD2Yolo.py --data .\datasets\CCPD\images\train_ccpd_base  --output .\datasets\CCPD\labels\train_ccpd_base
python CCPD2Yolo.py --data .\datasets\CCPD\images\val_ccpd_base    --output .\datasets\CCPD\labels\val_ccpd_base
python CCPD2Yolo.py --data .\datasets\CCPD\images\test_ccpd_base   --output .\datasets\CCPD\labels\test_ccpd_base


# Train customer data
python train.py --img 1088 --rect --batch 64 --epochs 6 --data ccpd_ds.yaml --weights yolov5s.pt

# Inference
python detect.py --weights last.pt --img 1024 --conf 0.25 --source data/images/ --save-crop

# Export
python export.py --weights yolov5s.pt  --batch 1 --include torchscript --optimize --inplace
