#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Set, Tuple, Optional
from wsp_lib.graph_base import State, Action


class DFSSearcher:
    """
    深さ優先探索を実行するクラス
    """
    
    def __init__(self, initial_state: State):
        """
        初期化
        
        Args:
            initial_state: 探索の初期状態
        """
        self.initial_state = initial_state
        self.visited_states: Set[State] = set()
        self.path_to_goal: List[Tuple[State, Optional[Action]]] = []
    
    def search(self, max_depth: int = -1) -> bool:
        """
        深さ優先探索を実行する
        
        Args:
            max_depth: 最大探索深度（デフォルトは-1で無制限）
            
        Returns:
            ゴールが見つかればTrue、そうでなければFalse
        """
        self.visited_states.clear()
        self.path_to_goal.clear()
        
        return self._dfs(self.initial_state, None, 0, max_depth)
    
    def _dfs(self, state: State, action: Optional[Action], depth: int, max_depth: int) -> bool:
        """
        再帰的に深さ優先探索を実行する内部メソッド
        
        Args:
            state: 現在の状態
            action: 直前のアクション
            depth: 現在の深さ
            max_depth: 最大探索深度
            
        Returns:
            ゴールが見つかればTrue、そうでなければFalse
        """
        # 訪問済みの状態はスキップ
        if state in self.visited_states:
            return False
        
        # 状態を訪問済みにマーク
        self.visited_states.add(state)
        
        # パスに追加
        self.path_to_goal.append((state, action))
        
        # ゴール状態なら探索終了
        if state.is_goal():
            return True
        
        # 最大深度に達したら探索終了
        if max_depth >= 0 and depth >= max_depth:
            self.path_to_goal.pop()
            return False
        
        # 可能なアクションをすべて試す
        for next_action in state.get_possible_actions():
            next_state = state.apply_action(next_action)
            
            # 再帰的に探索
            if self._dfs(next_state, next_action, depth + 1, max_depth):
                return True
        
        # ゴールが見つからなかったら、このパスは破棄
        self.path_to_goal.pop()
        return False
    
    def get_solution(self) -> List[Tuple[State, Optional[Action]]]:
        """
        探索で見つかった解を返す
        
        Returns:
            状態とアクションのペアのリスト
        """
        return self.path_to_goal 