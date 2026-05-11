import pandas as pd
import os

def convert_kicad_to_jlc(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} が見つかりません。")
        return

    # KiCadのPOSファイルを読み込み
    df = pd.read_csv(input_file)

    # 1. 列名のマッピング (KiCad -> JLCPCB)
    # JLCは 'Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation' を最低限必要とする
    column_map = {
        'Ref': 'Designator',
        'PosX': 'Mid X',
        'PosY': 'Mid Y',
        'Rot': 'Rotation',
        'Side': 'Layer'
    }
    
    # 存在する列だけリネーム
    df = df.rename(columns=column_map)

    # 2. レイヤー名のフォーマット修正 (bottom -> Bottom / top -> Top)
    if 'Layer' in df.columns:
        df['Layer'] = df['Layer'].str.capitalize()

    # 3. JLCPCBで不要な引用符を整理し、必要な列順で出力
    # 並び順は任意ですが、推奨される標準的な順序に整えます
    output_columns = ['Designator', 'Val', 'Package', 'Mid X', 'Mid Y', 'Rotation', 'Layer']
    
    # 存在する列のみ抽出
    existing_cols = [col for col in output_columns if col in df.columns]
    df_jlc = df[existing_cols]

    # 保存
    df_jlc.to_csv(output_file, index=False)
    print(f"Success: {output_file} を出力しました。")

if __name__ == "__main__":
    convert_kicad_to_jlc('yuho-all-pos.csv', 'jlc_pos.csv')