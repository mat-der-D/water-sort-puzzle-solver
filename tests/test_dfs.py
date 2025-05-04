#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from typing import List, Optional, Dict

from wsp_lib.graph_base import State, Action
from wsp_lib.dfs import DFSSearcher


class MockAction(Action):
    """
    テスト用のアクションモック
    """
    
    def __init__(self, name: str):
        """
        初期化
        
        Args:
            name: アクションの名前
        """
        self.name = name
    
    def __str__(self) -> str:
        return f"Action({self.name})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MockAction):
            return False
        return self.name == other.name
    
    def __hash__(self) -> int:
        return hash(self.name)


class MockState(State):
    """
    テスト用の状態モック
    """
    # テスト用の状態グラフを管理するクラス変数
    state_graph: Dict[int, 'MockState'] = {}
    
    def __init__(self, value: int, is_goal_state: bool = False, transitions=None):
        """
        初期化
        
        Args:
            value: 状態の値
            is_goal_state: ゴール状態かどうか
            transitions: 可能な遷移のリスト [(アクション名, 次の状態の値), ...]
        """
        self.value = value
        self._is_goal_state = is_goal_state
        self.transitions = transitions or []
        
        # クラス変数の状態グラフに自身を登録
        MockState.state_graph[value] = self
    
    @classmethod
    def clear_state_graph(cls):
        """
        状態グラフをクリアするクラスメソッド
        """
        cls.state_graph.clear()
    
    def get_possible_actions(self) -> List[Action]:
        return [MockAction(action_name) for action_name, _ in self.transitions]
    
    def is_goal(self) -> bool:
        return self._is_goal_state
    
    def apply_action(self, action: Action) -> 'State':
        if not isinstance(action, MockAction):
            raise ValueError("Invalid action type")
        
        for action_name, next_state_value in self.transitions:
            if action_name == action.name:
                # クラス変数の状態グラフから次の状態を取得
                if next_state_value in MockState.state_graph:
                    return MockState.state_graph[next_state_value]
                
                # 存在しない場合は新しく作成
                new_state = MockState(next_state_value)
                return new_state
        
        raise ValueError(f"Invalid action: {action}")
    
    def is_valid_action(self, action: Action) -> bool:
        if not isinstance(action, MockAction):
            return False
        
        for action_name, _ in self.transitions:
            if action_name == action.name:
                return True
        
        return False
    
    def __str__(self) -> str:
        return f"State({self.value})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MockState):
            return False
        return self.value == other.value
    
    def __hash__(self) -> int:
        return hash(self.value)


class TestDFSSearcher(unittest.TestCase):
    """
    DFSSearcherのテストクラス
    """
    
    def setUp(self):
        """
        各テストケース実行前の準備
        """
        # 状態グラフをクリア
        MockState.clear_state_graph()
    
    def test_search_finds_goal(self):
        """
        search()メソッドがゴールを見つけることをテスト
        """
        # 状態グラフを作成: 0 -> 1 -> 2 (ゴール)
        # 状態0: 初期状態
        state0 = MockState(0, False, [
            ("move_to_1", 1)
        ])
        
        # 状態1: 中間状態
        state1 = MockState(1, False, [
            ("move_to_2", 2)
        ])
        
        # 状態2: ゴール状態
        state2 = MockState(2, True)
        
        # 探索器を作成して実行
        searcher = DFSSearcher(state0)
        result = searcher.search()
        
        # ゴールが見つかることを確認
        self.assertTrue(result)
        
        # 探索パスが正しいことを確認
        solution = searcher.get_solution()
        self.assertEqual(len(solution), 3)
        
        # 初期状態のチェック
        self.assertEqual(solution[0][0].value, 0)
        self.assertIsNone(solution[0][1])
        
        # 中間状態のチェック
        self.assertEqual(solution[1][0].value, 1)
        self.assertEqual(solution[1][1].name, "move_to_1")
        
        # ゴール状態のチェック
        self.assertEqual(solution[2][0].value, 2)
        self.assertEqual(solution[2][1].name, "move_to_2")
    
    def test_search_no_goal(self):
        """
        ゴールが存在しない場合のsearch()メソッドをテスト
        """
        # ゴールがない状態グラフを作成: 0 -> 1 -> 0 (ループ)
        state0 = MockState(0, False, [
            ("move_to_1", 1)
        ])
        
        state1 = MockState(1, False, [
            ("move_to_0", 0)
        ])
        
        # 探索器を作成して実行
        searcher = DFSSearcher(state0)
        result = searcher.search()
        
        # ゴールが見つからないことを確認
        self.assertFalse(result)
        
        # 解が空であることを確認
        solution = searcher.get_solution()
        self.assertEqual(len(solution), 0)
    
    def test_search_with_max_depth(self):
        """
        最大深度を指定した場合のsearch()メソッドをテスト
        """
        # 状態グラフを作成: 0 -> 1 -> 2 (ゴール)
        state0 = MockState(0, False, [
            ("move_to_1", 1)
        ])
        
        state1 = MockState(1, False, [
            ("move_to_2", 2)
        ])
        
        state2 = MockState(2, True)
        
        # 探索器を作成して、深度1で実行（ゴールに届かない）
        searcher = DFSSearcher(state0)
        result = searcher.search(max_depth=1)
        
        # 深度が足りないためゴールが見つからないことを確認
        self.assertFalse(result)
        
        # 深度2で実行（ゴールに届く）
        result = searcher.search(max_depth=2)
        
        # ゴールが見つかることを確認
        self.assertTrue(result)
        
        # 探索パスが正しいことを確認
        solution = searcher.get_solution()
        self.assertEqual(len(solution), 3)
    
    def test_multiple_search_calls(self):
        """
        searchを複数回呼び出した場合のテスト
        """
        # 状態グラフを作成: 0 -> 1 -> 2 (ゴール)
        state0 = MockState(0, False, [
            ("move_to_1", 1)
        ])
        
        state1 = MockState(1, False, [
            ("move_to_2", 2)
        ])
        
        state2 = MockState(2, True)
        
        # 探索器を作成して実行
        searcher = DFSSearcher(state0)
        
        # 1回目の検索
        result1 = searcher.search()
        self.assertTrue(result1)
        solution1 = searcher.get_solution()
        
        # 2回目の検索（訪問済み状態がリセットされるはず）
        result2 = searcher.search()
        self.assertTrue(result2)
        solution2 = searcher.get_solution()
        
        # 両方の解が同じであることを確認
        self.assertEqual(len(solution1), len(solution2))
        for i in range(len(solution1)):
            self.assertEqual(solution1[i][0].value, solution2[i][0].value)
            if i > 0:  # 初期状態のアクションはNone
                self.assertEqual(solution1[i][1].name, solution2[i][1].name)


if __name__ == "__main__":
    unittest.main() 