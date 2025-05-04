#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from wsp_lib.wsp_graph import WSPAction, WSPState


class TestWSPAction(unittest.TestCase):
    """
    WSPActionクラスのテスト
    """
    
    def test_init(self):
        """
        初期化が正しく行われるかテスト
        """
        action = WSPAction(0, 1)
        self.assertEqual(action.from_tube, 0)
        self.assertEqual(action.to_tube, 1)
    
    def test_str(self):
        """
        文字列表現が正しいかテスト
        """
        action = WSPAction(0, 1)
        self.assertEqual(str(action), "チューブ0からチューブ1へ水を移動")
    
    def test_eq(self):
        """
        等価演算子が正しく動作するかテスト
        """
        action1 = WSPAction(0, 1)
        action2 = WSPAction(0, 1)
        action3 = WSPAction(1, 0)
        
        self.assertEqual(action1, action2)
        self.assertNotEqual(action1, action3)
        self.assertNotEqual(action1, "not_an_action")
    
    def test_hash(self):
        """
        ハッシュ値が一貫しているかテスト
        """
        action1 = WSPAction(0, 1)
        action2 = WSPAction(0, 1)
        
        self.assertEqual(hash(action1), hash(action2))
        
        # 異なるアクションは異なるハッシュ値を持つ可能性が高い
        # ただし、ハッシュの衝突の可能性もあるため、必ずしも異なるとは限らない
        action3 = WSPAction(1, 0)
        self.assertNotEqual(hash(action1), hash(action3))


class TestWSPState(unittest.TestCase):
    """
    WSPStateクラスのテスト
    """
    
    def setUp(self):
        """
        テスト用の状態を準備
        """
        # 基本的なテスト用状態
        self.state1 = WSPState([
            ["赤", "青", "緑"],
            ["青", "赤"],
            ["緑"],
            []
        ])
        
        # ゴール状態に近い状態
        self.goal_state = WSPState([
            ["赤", "赤", "赤", "赤"],
            ["青", "青", "青", "青"],
            ["緑", "緑", "緑", "緑"],
            []
        ])
    
    def test_init(self):
        """
        初期化が正しく行われるかテスト
        """
        state = WSPState([["赤"], ["青"]], 3)
        self.assertEqual(state.tubes, [["赤"], ["青"]])
        self.assertEqual(state.max_tube_capacity, 3)
    
    def test_get_possible_actions(self):
        """
        可能なアクションが正しく列挙されるかテスト
        """
        # 簡単な状態での可能なアクション
        simple_state = WSPState([
            ["赤"],  # チューブ0
            []       # チューブ1（空）
        ])
        
        actions = simple_state.get_possible_actions()
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0], WSPAction(0, 1))
        
        # もっと複雑な状態
        # 最上部の色が同じチューブへの移動だけが可能
        complex_state = WSPState([
            ["赤", "青"],        # チューブ0
            ["青"],              # チューブ1
            ["緑"],              # チューブ2
            []                  # チューブ3（空）
        ])
        
        actions = complex_state.get_possible_actions()
        expected_actions = [
            WSPAction(0, 1),  # チューブ0から同じ色（青）のあるチューブ1へ
            WSPAction(0, 3),  # チューブ0から空のチューブ3へ
            WSPAction(1, 0),  # チューブ1から同じ色（青）のあるチューブ0へ
            WSPAction(1, 3),  # チューブ1から空のチューブ3へ
            WSPAction(2, 3)   # チューブ2から空のチューブ3へ
        ]
        
        self.assertEqual(len(actions), len(expected_actions))
        for action in expected_actions:
            self.assertIn(action, actions)
    
    def test_is_goal(self):
        """
        ゴール状態の判定が正しく行われるかテスト
        """
        # 非ゴール状態
        self.assertFalse(self.state1.is_goal())
        
        # 部分的に完成した状態（まだゴールではない）
        partial_goal = WSPState([
            ["赤", "赤", "赤", "赤"],  # 完成
            ["青", "青", "青"],        # 未完成
            ["緑", "緑", "緑", "緑"],  # 完成
            []                        # 空（OK）
        ])
        self.assertFalse(partial_goal.is_goal())
        
        # ゴール状態
        self.assertTrue(self.goal_state.is_goal())
    
    def test_apply_action(self):
        """
        アクションの適用が正しく行われるかテスト
        """
        # 単純な移動テスト
        state = WSPState([
            ["赤", "青"],  # チューブ0
            []            # チューブ1
        ])
        
        action = WSPAction(0, 1)
        new_state = state.apply_action(action)
        
        expected_state = WSPState([
            ["赤"],       # チューブ0
            ["青"]        # チューブ1
        ])
        
        self.assertEqual(new_state, expected_state)
        
        # 同じ色の連続した水の移動テスト
        state = WSPState([
            ["赤", "青", "青"],  # チューブ0
            []                  # チューブ1
        ])
        
        action = WSPAction(0, 1)
        new_state = state.apply_action(action)
        
        expected_state = WSPState([
            ["赤"],            # チューブ0
            ["青", "青"]       # チューブ1
        ])
        
        self.assertEqual(new_state, expected_state)
        
        # 容量制限のテスト
        state = WSPState([
            ["赤", "青", "青", "青"],  # チューブ0（満杯）
            ["青"]                    # チューブ1
        ], max_tube_capacity=4)
        
        action = WSPAction(1, 0)
        
        # 容量オーバーになるので例外が発生するはず
        with self.assertRaises(ValueError):
            state.apply_action(action)
    
    def test_is_valid_action(self):
        """
        アクションの有効性判定が正しく行われるかテスト
        """
        # 有効なアクション
        state = WSPState([
            ["赤", "青"],  # チューブ0
            []            # チューブ1
        ])
        
        valid_action = WSPAction(0, 1)
        self.assertTrue(state.is_valid_action(valid_action))
        
        # 無効なアクション（異なる色の上に置けない）
        state = WSPState([
            ["赤", "青"],  # チューブ0
            ["緑"]         # チューブ1
        ])
        
        invalid_action = WSPAction(0, 1)
        self.assertFalse(state.is_valid_action(invalid_action))
        
        # 無効なアクション（チューブが満杯）
        state = WSPState([
            ["赤"],                    # チューブ0
            ["青", "青", "青", "青"]   # チューブ1（満杯）
        ], max_tube_capacity=4)
        
        invalid_action = WSPAction(0, 1)
        self.assertFalse(state.is_valid_action(invalid_action))
        
        # 無効なアクション（空のチューブから移動しようとする）
        state = WSPState([
            [],      # チューブ0（空）
            ["青"]   # チューブ1
        ])
        
        invalid_action = WSPAction(0, 1)
        self.assertFalse(state.is_valid_action(invalid_action))
        
        # 無効なアクション（範囲外のインデックス）
        state = WSPState([
            ["赤"],   # チューブ0
            ["青"]    # チューブ1
        ])
        
        invalid_action = WSPAction(0, 2)  # チューブ2は存在しない
        self.assertFalse(state.is_valid_action(invalid_action))
    
    def test_str(self):
        """
        文字列表現が正しいかテスト
        """
        state = WSPState([
            ["赤", "青"],
            []
        ])
        
        expected_str = "チューブ0: [赤,青]\nチューブ1: [空]"
        self.assertEqual(str(state), expected_str)
    
    def test_eq(self):
        """
        等価演算子が正しく動作するかテスト
        """
        state1 = WSPState([
            ["赤", "青"],
            ["緑"]
        ])
        
        state2 = WSPState([
            ["赤", "青"],
            ["緑"]
        ])
        
        state3 = WSPState([
            ["緑"],
            ["赤", "青"]
        ])
        
        # 同じ内容のチューブを持つ状態は等しい
        self.assertEqual(state1, state2)
        
        # チューブの順序が異なる場合も等しい（チューブの順序は重要でない）
        self.assertEqual(state1, state3)
        
        # 異なる内容のチューブを持つ状態は等しくない
        state4 = WSPState([
            ["赤", "青"],
            ["黄"]
        ])
        
        self.assertNotEqual(state1, state4)
        
        # 異なる型のオブジェクトとは等しくない
        self.assertNotEqual(state1, "not_a_state")
    
    def test_hash(self):
        """
        ハッシュ値が一貫しているかテスト
        """
        state1 = WSPState([
            ["赤", "青"],
            ["緑"]
        ])
        
        state2 = WSPState([
            ["赤", "青"],
            ["緑"]
        ])
        
        state3 = WSPState([
            ["緑"],
            ["赤", "青"]
        ])
        
        # 同じ内容の状態は同じハッシュ値を持つ
        self.assertEqual(hash(state1), hash(state2))
        
        # チューブの順序が異なる場合も同じハッシュ値を持つべき
        self.assertEqual(hash(state1), hash(state3))
        
        # 異なる内容の状態は異なるハッシュ値を持つ可能性が高い
        state4 = WSPState([
            ["赤", "青"],
            ["黄"]
        ])
        
        self.assertNotEqual(hash(state1), hash(state4))


if __name__ == "__main__":
    unittest.main()