#!/usr/local/bin/python3

import pandas as pd


def dict_to_md(dc,
               title="TOP", depth=1, format="md", compress=False):
    """
    dict(もしくは list) を 見出し付き Markdownテーブルに変換する

    Args:
        dc ([type]): 変換対象の (dict, もしくは list)
        title (str, optional): トップ見出しのタイトル. Defaults to "TOP".
        depth (int, optional): トップ見出しの深さ. Defaults to 1.
        format (str, optional): 見出しのフォーマット ("md" もしくは "org") . Defaults to "md".
    """
    # format (md or org)
    head_str = "*" if format == "org" else "#"
    # データ変換
    items = []
    if type(dc) == dict:
        # dict は items() へ変換
        items = dc.items()
    elif type(dc) == list:
        # list は タプルリストへ変換
        items = [("#{}".format(i+1), v) for i, v in enumerate(dc)]
    # 表示可能アイテム、表示不可能アイテムに分類
    displayable = [(k, v) for k, v in items if type(v) not in [dict, list]]
    not_displayable = [(k, v) for k, v in items if type(v) in [dict, list]]
    # 見出しを print
    print("{} {}".format(head_str * depth, title))
    # 表示可能アイテムを print
    if displayable:
        print(pd.DataFrame(displayable,
                           columns=["key", "value"]).to_markdown(showindex=False))
    # 表示不可能アイテムを parse
    for k, v in not_displayable:
        dict_to_md(v, title=k, depth=depth+1, format=format, compress=compress)


if __name__ == "__main__":
    sample = {
        "key1": "value1",
        "key2": "value2",
        "map-value": {
            "key3-1": "value3-1",
            "key3-2": "value3-2",
        },
        "list-value": [
            "aaa",
            "bbb",
            "ccc",
        ],
        "Tags": [
            {"Key": "Name",  "Value": "my-instance"},
            {"Key": "Owner", "Value": "taro"},
        ]
    }
    dict_to_md(sample)
