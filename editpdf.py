#! python3
from datetime import date
import re
import glob
from PyPDF2 import PdfReader, PdfWriter, PdfMerger, PageRange
import fire

TODAY: str = date.today().isoformat()

def cat(*infiles: str, output: str = f'{TODAY}_output.pdf', overwrite=False, bookmark=True):
    """PDFファイルの結合、分割

    Args:
        inputs (tuple[str]): 'filename' または 'filename[start:stop:step]'. 例: awesome、awesome.pdf[1:5]
        output (str, optional): 結合後のファイル名. Defaults to 'yyyy-mm-dd_output.pdf'.
        overwrite (bool, optional): 値をTrueにすることでファイルの上書きを許可する. Defaults to False.
        bookmark (bool, optional): ブックマークを自動的に追加する. Defaults to True.
        ブックマークを追加しない場合は、--nobookmarkまたは--bookmark=Falseを引数にとる.
    """

    # 引数の処理
    _INT_RE = r"(0|-?[1-9]\d*)"
    PAGE_RANGE_RE = fr"({_INT_RE}|({_INT_RE}?(:{_INT_RE}?(:{_INT_RE}?)?)))"
    PAGE_PROG = re.compile(fr'\[{PAGE_RANGE_RE}\]$') # ページ範囲（例: [3:7], [:-1]）を表す正規表現

    files: list[str] = []
    page_ranges: list[PageRange] = []
    for infile in infiles:
        # ページ範囲の文字列を解析する
        result = PAGE_PROG.search(infile)
        res_str = result.group() if result else ':'

        # ファイル名はglob関数で処理
        fe = infile.rstrip(res_str)
        fe = fe if fe[-4:].lower()=='.pdf' else f'{fe}.pdf'
        filenames: list = glob.glob(fe, dir_fd=None)

        # ページ範囲はPageRangeオブジェクトを作る
        page_range = PageRange(res_str.lstrip('[').rstrip(']'))
        for filename in filenames:
            # ファイル名が「*講義資料.pdf」のような場合、
            # PageRangeオブジェクトをマッチするファイルの数だけ増やして用意しなければならない
            files.append(filename)
            page_ranges.append(page_range)

    mode: str = 'wb' if overwrite else 'xb'
    message: str = 'ファイルは正常に書き込まれました。' if overwrite else 'ファイルは正常に作成されました。'

    # Mergerオブジェクトの処理
    merger = PdfMerger()
    if len(infiles) == 1:
        bookmark = False
    for file, page_range in zip(files, page_ranges):
        reader = PdfReader(file)
        outline_item = f'{file[:-4]}' if bookmark else None
        merger.append(reader, outline_item=outline_item, pages=page_range)

    # ファイルの書き込み
    output = output if output[-4:].lower()=='.pdf' else f'{output}.pdf'
    with open(output, mode=mode) as f:
        merger.write(f)

    # メッセージの出力
    print(message)


def bm(
        infile: str, title: str, pagenum: int,
        outfile: str = f'{TODAY}_output.pdf', overwrite=False
):
    """PDFファイルにブックマークを追加

    Args:
        input (str): 入力するPDFファイル名
        title (str): ブックマークのタイトル
        pagenum (int): ブックマークを追加するページ番号
        output (str, optional): _description_. Defaults to 'yyyy-mm-dd_output.pdf'.
        overwrite (bool, optional): Trueの場合、元のファイルへの上書きを許可する. Defaults to False.
    """
    infile = infile if infile[-4:].lower()=='.pdf' else f'{infile}.pdf'
    mode: str = 'wb' if overwrite else 'xb'
    reader = PdfReader(infile)
    writer = PdfWriter()

    writer.clone_document_from_reader(reader=reader)
    writer.add_outline_item(title, pagenum-1)

    outfile = outfile if outfile[-4:].lower()=='.pdf' else f'{outfile}.pdf'
    with open(outfile, mode=mode) as f:
        writer.write(f)
    
    # メッセージの出力
    print('ブックマークは正常に追加されました。')

def dec(infile: str, pw: str = '', outfile: str = f'{TODAY}_output.pdf', overwrite=False):
    """PDFファイルの暗号化解除 (未完)

    Args:
        infile (str): 入力するPDFファイル名
        pw (str, optional): 入力PDFファイルのパスワード. デフォルトで''.
        outfile (str, optional): 出力ファイル名. デフォルトで f'{TODAY}_output.pdf'.
        overwrite (bool, optional): Trueの場合、元のファイルへの上書きを許可する. Defaults to False.
    """
    mode: str = 'wb' if overwrite else 'xb'
    reader = PdfReader(infile, password=pw)
    writer = PdfWriter()

    # if reader.is_encrypted:
    #     reader.decrypt(pw)

    writer.clone_document_from_reader(reader=reader)

    with open(outfile, mode=mode) as f:
        writer.write(f)

if __name__ == '__main__':
    fire.Fire()
