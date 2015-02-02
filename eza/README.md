# eza

引数で指定したファイル、ディレクトリをカレントディレクトリの "archive" に移動する。

## archive ディレクトリ

"archive" ディレクトリ内は実行時の日付けを "yyyy-MM-dd" と言う書式でサブディレクトリが作成され、指定したファイル、ディレクトリはその日付けのサブディレクトリ内に移動される。

## archive ディレクトリのアイコン

環境変数 EZA_FOLDER_ICON にアイコンの指定を設定しておくと、archive ディレクトリ作成時にカスタムアイコンとして設定される。

※作成時のみ。既に archive ディレクトリが存在する場合に更新されたりはしない。

### 例
```Batchfile
SET EZA_FOLDER_ICON=%SystemRoot%\system32\SHELL32.dll,0
```
