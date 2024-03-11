import os
import pandas as pd
from PIL import Image
import piexif

def convert_rational_to_decimal(rational_latlon):
    ((deg_nmr, deg_dnm), (min_nmr, min_dnm), (sec_nmr, sec_dnm)) = rational_latlon
    return deg_nmr / deg_dnm + min_nmr / min_dnm / 60 + sec_nmr / sec_dnm / 3600

def resize_and_convert_image(input_dir, output_dir, size=(1280, 720)):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    metadata_list = []
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".jpg"):
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + '.jpg'
            output_path = os.path.join(output_dir, output_filename)

            # 画像を開き、リサイズする
            image = Image.open(input_path)
            image = image.resize(size)

            # EXIFデータをコピーする
            exif_data = piexif.load(image.info['exif'])
            # 緯度経度情報を抽出（ダミーデータを使用。実際にはEXIFから読み取る必要がある）
            latitude = convert_rational_to_decimal(exif_data.get('GPS', {}).get(piexif.GPSIFD.GPSLatitude, (0, 0, 0)))
            longitude = convert_rational_to_decimal(exif_data.get('GPS', {}).get(piexif.GPSIFD.GPSLongitude, (0, 0, 0)))
            
            # JPEGとして保存
            image.save(output_path, "JPEG", exif=piexif.dump(exif_data))
            
            # メタデータリストに情報を追加
            metadata_list.append({
                "filename": output_filename,
                "latitude": latitude,
                "longitude": longitude,
                "comment": filename
            })

    # CSVファイルを作成
    metadata_df = pd.DataFrame(metadata_list)
    metadata_df.to_csv(os.path.join(output_dir, "photos_metadata.csv"), index=False)


# フォルダパスとサイズを指定
input_dir = r'D:\OneDrive - nagaokaut.ac.jp\01_Research\01_Field Survey\06_202401_Noto\01_2024-01-02_04_第1回調査\2024-01-02\image_shiga_resize'
output_dir = r"D:\OneDrive - nagaokaut.ac.jp\01_Research\01_Field Survey\06_202401_Noto\01_2024-01-02_04_第1回調査\2024-01-02\image_shiga_resize_2"
size = (1280, 720)  # 例えば1280x720にリサイズ

resize_and_convert_image(input_dir, output_dir, size)
