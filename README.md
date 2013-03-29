ts-watch
========

TypeScript development server

## これはなに？

エディタだけでTypeScriptを使って、ブラウザで確認を繰り返していると、tsコンパイルするのを忘れてリロードだけしてしまうことが多かったので、Webサーバとtypescriptの変更検出、自動コンパイルを行うようにするサーバ。

 - 簡易WebServer - 実行ディレクトリをドキュメントルートに.
 - typescriptの自動コンパイル - 配下のファイルの更新を検出して再コンパイル


## 実行方法

    $ python ts-watch.py
    Start HTTPServer port 8000 ...


