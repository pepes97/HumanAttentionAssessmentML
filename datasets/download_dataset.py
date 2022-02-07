import argparse
import os
import zipfile
import gdown

'''
Download and extract the standard dataset, face detection dataset or GAN dataset 
into a defined directory (standard_dataset, face_detection_dataset or GAN_dataset directory).
Command line arguments define which dataset partition to download
'''


def download_dataset(set_type):
  URL_train = ""
  URL_dev = ""
  URL_test = ""
  if set_type == "standard":

    dataset_path = "standard_dataset"
    if not os.path.exists(os.getcwd()+os.sep+dataset_path+os.sep):
      os.mkdir(os.getcwd()+os.sep+dataset_path+os.sep)
      
    URL_train = 'https://drive.google.com/uc?export=download&id=1QZvZEnovbfbQxxZ3Q-v-LenvHf4RQQ1T'
    URL_dev = "https://drive.google.com/uc?export=download&id=1-125OQ66bsJPHa3chQi7khng1Nx2Hn7E"
    URL_test = "https://drive.google.com/uc?export=download&id=1-5Nfa7KamMMvtxwVZGtLi6b1hR8zCh-k"
  
  elif set_type=="face_detection":

    dataset_path = "face_detection_dataset"
    if not os.path.exists(os.getcwd()+os.sep+dataset_path+os.sep):
      os.mkdir(os.getcwd()+os.sep+dataset_path+os.sep)
    URL_train = "https://drive.google.com/uc?export=download&id=1u57z2B_Kdwtzly1p0gEwm9bQ60AUeM7j"
    URL_dev = "https://drive.google.com/uc?export=donwload&id=1-0uFU0xH2swwQXVE7uGR1tCa7dtkshgd"
    URL_test = "https://drive.google.com/uc?export=download&id=1-5B1d2UJNQvqY1eFIr7_DT8NngMZNboR"
  
  elif set_type=="GAN":

    dataset_path = "GAN_dataset"
    if not os.path.exists(os.getcwd()+os.sep+dataset_path+os.sep):
      os.mkdir(os.getcwd()+os.sep+dataset_path+os.sep)

    URL_train = "https://drive.google.com/uc?export=download&id=17ftWHpb8Crug4yMXgJnixRDimwmccFJ1"
    URL_dev = "https://drive.google.com/uc?export=download&id=1-28h7LIbC59Z-m_FcIzCfopeQR4k7z4Q"
    URL_test = "https://drive.google.com/uc?export=download&id=1-GoExOM4nWwBXFmkIG0DJeELEHHY1GkI"
  
  else:
    print("Type not valid. ")
    print(f"available type are: \t standard or \t face_detection")
    exit(0)

  if not os.path.exists(os.getcwd()+os.sep+dataset_path+os.sep+"train.zip"):
    if not os.path.exists(os.getcwd()+os.sep+dataset_path+os.sep+"dev.zip"):
      if not os.path.exists(os.getcwd()+os.sep+dataset_path+os.sep+"test.zip"):
        print ('Downloading train, dev, test')
        gdown.download(URL_train, os.getcwd()+os.sep+dataset_path+os.sep+"train.zip", quiet=False)
        gdown.download(URL_dev, os.getcwd()+os.sep+dataset_path+os.sep+"dev.zip", quiet=False)
        gdown.download(URL_test, os.getcwd()+os.sep+dataset_path+os.sep+"test.zip", quiet=False)
        extract_dataset(dataset_path)
        print("\n")

def extract_dataset(dataset_path):
  if os.path.exists(os.getcwd()+os.sep+dataset_path+os.sep+"train.zip"):
    print("Extracting the archive")
    with zipfile.ZipFile(os.getcwd()+os.sep+dataset_path+os.sep+'train.zip', 'r') as zip_ref:
      zip_ref.extractall(os.getcwd()+os.sep+dataset_path+os.sep)
    with zipfile.ZipFile(os.getcwd()+os.sep+dataset_path+os.sep+'dev.zip', 'r') as zip_ref:
      zip_ref.extractall(os.getcwd()+os.sep+dataset_path+os.sep)
    with zipfile.ZipFile(os.getcwd()+os.sep+dataset_path+os.sep+'test.zip', 'r') as zip_ref:
      zip_ref.extractall(os.getcwd()+os.sep+dataset_path+os.sep)
    print("Done")
    os.remove(os.getcwd()+os.sep+dataset_path+os.sep+"train.zip")   
    os.remove(os.getcwd()+os.sep+dataset_path+os.sep+"dev.zip") 
    os.remove(os.getcwd()+os.sep+dataset_path+os.sep+"test.zip")
    print("Zips removed")      

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--set_type', type=str,
                        help='which set to download, "standard", "face_detection" or "GAN" dataset')


    args = parser.parse_args()
    if args.set_type is None:
      print(f'The insterted type is not valid.')
      print(f"Available type are: \033[1mstandard\033[0m, \033[1mface_detection\033[0m or \033[1mGAN\033[0m")
      exit(0)

    download_dataset(args.set_type)
