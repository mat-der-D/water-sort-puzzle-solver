#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from wsp_lib.wsp_graph import WSPState, WSPAction
from wsp_lib.dfs import DFSSearcher


def main():
    """
    Water Sort Puzzleの初期状態を設定し、深さ優先探索を行い、結果を表示する
    """
    # 初期状態の設定
    # 各チューブの中の色水を表現（下から上へ順に記述）
    tubes = [
        ["赤", "赤", "緑", "黄"],
        ["黄", "緑", "黄", "緑"],
        ["赤", "赤", "黄", "緑"],
        [],
        [],
    ]
    
    # 初期状態を作成
    initial_state = WSPState(tubes)
    
    # 初期状態の表示
    print("【初期状態】")
    print(initial_state)
    print()
    
    # 深さ優先探索の実行
    searcher = DFSSearcher(initial_state)
    result = searcher.search()
    
    # 探索結果の表示
    if result:
        path = searcher.get_solution()
        print(f"【解決策が見つかりました！ステップ数: {len(path) - 1}】")
        
        # 各ステップを表示
        for i, (state, action) in enumerate(path):
            if i == 0:
                print(f"開始状態:")
            else:
                print(f"ステップ {i}:")
                print(f"アクション: {action}")
            print(state)
            print()
    else:
        print("【解決策が見つかりませんでした】")
    
    print(f"探索した状態の数: {len(searcher.visited_states)}")


if __name__ == "__main__":
    main()