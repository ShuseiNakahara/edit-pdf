# edit-pdf
[PyPDF2](https://pypdf2.readthedocs.io/en/latest/)と[python-fire](https://github.com/google/python-fire)を利用したPython製のPDF編集コマンドラインアプリケーションです。

## インストール
1. `editpdf.py`をダウンロードします。
2. 依存しているサードパーティ製ライブラリをインストールします。
```bash
pip install PyPDF2 fire
```
3. `editpdf.py`と同じディレクトリで`python editpdf.py --help`を実行し、起動できるかを確認します。

## 使用方法
現在実装している機能とその使用方法について説明します。

### 概要
```bash
python editpdf.py command <flags> [args]
```
このファイルのパスを通した場合、最初の`python`を省略してどの場所でも使用できるようになります。Windowsユーザはそのためにバッチファイル`editpdf.bat`を使用できます。

### cat - 結合、分割
```
NAME
    editpdf.py cat - PDFファイルの結合、分割

SYNOPSIS
    editpdf.py cat <flags> [INFILES]...

DESCRIPTION
    PDFファイルの結合、分割

POSITIONAL ARGUMENTS
    INFILES
        Type: str

FLAGS
    --output=OUTPUT
        Type: str
        Default: 'yyyy-mm-dd_output.pdf'
        結合後のファイル名
    --overwrite=OVERWRITE
        Default: False
        値をTrueにすることでファイルの上書きを許可する. Defaults to False.
    -b, --bookmark=BOOKMARK
        Default: True
        ブックマークを自動的に追加する. Defaults to True. ブックマークを追加しない場合は、--nobookmarkまたは--bookmark=Falseを引数にとる.
```

上記と同じ内容は、`python editpdf.py cat --help`を実行することで確認できます。

例: `doc1.pdf`と`doc2.pdf`を結合する。
```
python editpdf.py cat doc1.pdf doc2.pdf
```
`editpdf.py`と同じディレクトリに今日の日付で`yyyy-mm-dd_output.pdf`が作成されます。拡張子`.pdf`は省略することもできます。

例: `doc1.pdf`の1ページ目を取り出す。
```
python editpdf.py cat doc1[0]
```
ファイル名を引数にとるとき、Pythonと同様のスライス構文が使用できます (注: **0始まりとなります**)。
