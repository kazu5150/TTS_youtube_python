# 参考にさせてもらったXの投稿
https://x.com/kk_design_dev/status/1841072793221566484

## テキストから音声への変換プロジェクト

このプロジェクトは、指定されたテキストを音声ファイル（MP3形式）に変換するPythonスクリプトを含んでいます。特に、複数のテキストセグメントを個別の音声ファイルに変換し、それらを一つの音声ファイルにマージする機能があります。
この例は、英語のYouTube動画から文字起こしをし、日本語に翻訳し{時間：テキスト}というjsonファイルをこのpythonコードに渡すと、音声ファイルを出力してくれます。

text.json:
{
    "00:00" : "今日はいい天気ですね",
    "01:05"  :"どこかに遊びに行きたくなります！",
    "01:39" : "綺麗な山を見に行きましょう！"
}
![input json example image](input_json_example_image.png)

### 特徴

- テキストを音声に変換
- 複数の音声セグメントの生成とマージ
- 音声の速度調整機能
- 日本語の女性音声（Kyokoなど）を使用

### 必要条件

このスクリプトを実行するには、以下のライブラリが必要です。

- Python 3.6以上
- pydub
- ffmpeg（pydubのバックエンドとして必要）

### フォルダ構造

以下はこのプロジェクトのディレクトリ構造です：

```
プロジェクト名/
│
├── main.py                # メインスクリプト
├── requirements.txt       # 依存関係リスト
├── text.json              # 音声変換用テキストデータ
│
├── temp_audio/            # 一時音声ファイル保存用ディレクトリ
│
└── LICENSE                # ライセンスファイル
```

この構造は、プロジェクトの各コンポーネントがどのように配置されているかを示しています。`main.py`は音声変換のメインスクリプト、`requirements.txt`は必要なPythonライブラリをリストしています。`text.json`は変換するテキストデータを含み、`temp_audio`ディレクトリは生成された一時音声ファイルを保存します。

### セットアップ

1. このリポジトリをクローンします。
   ```
   git clone [リポジトリのURL]
   ```
2. 必要なライブラリをインストールします。
   ```
   pip install -r requirements.txt
   ```

### 使用方法

1. `text.json` ファイルに音声に変換したいテキストをJSON形式で保存します。
2. メインスクリプトを実行します。
   ```
   python main.py
   ```
3. 出力された `output.mp3` ファイルを確認します。

### ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。

### 貢献

プロジェクトへの貢献に興味がある方は、プルリクエストやイシューを通じて貢献してください。

