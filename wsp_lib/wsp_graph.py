#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Tuple, Optional
from copy import deepcopy
from wsp_lib.graph_base import State, Action


class WSPAction(Action):
    """
    Water Sort Puzzleのアクションクラス
    あるチューブから別のチューブへ水を移す操作を表す
    """
    
    def __init__(self, from_tube: int, to_tube: int):
        """
        初期化
        
        Args:
            from_tube: 水を移す元のチューブのインデックス
            to_tube: 水を移す先のチューブのインデックス
        """
        self.from_tube = from_tube
        self.to_tube = to_tube
    
    def __str__(self) -> str:
        """
        アクションの文字列表現を返す
        
        Returns:
            アクションの文字列表現
        """
        return f"チューブ{self.from_tube}からチューブ{self.to_tube}へ水を移動"
    
    def __eq__(self, other: object) -> bool:
        """
        2つのアクションが等しいかどうかを判定する
        
        Args:
            other: 比較対象のオブジェクト
            
        Returns:
            等しければTrue、そうでなければFalse
        """
        if not isinstance(other, WSPAction):
            return False
        return (self.from_tube == other.from_tube and 
                self.to_tube == other.to_tube)
    
    def __hash__(self) -> int:
        """
        アクションのハッシュ値を返す
        
        Returns:
            ハッシュ値
        """
        return hash((self.from_tube, self.to_tube))


class WSPState(State):
    """
    Water Sort Puzzleの状態クラス
    複数のチューブとその中の色水の状態を表す
    """
    
    def __init__(self, tubes: List[List[str]], max_tube_capacity: int = 4):
        """
        初期化
        
        Args:
            tubes: チューブのリスト（各チューブは色のリスト）
            max_tube_capacity: チューブの最大容量
        """
        self.tubes = tubes
        self.max_tube_capacity = max_tube_capacity
    
    def get_possible_actions(self) -> List[Action]:
        """
        この状態から実行可能なアクションのリストを返す
        
        Returns:
            実行可能なアクションのリスト
        """
        actions = []
        
        for from_idx in range(len(self.tubes)):
            for to_idx in range(len(self.tubes)):
                # 同じチューブには移動できない
                if from_idx == to_idx:
                    continue
                    
                # アクションを作成して有効性をチェック
                action = WSPAction(from_idx, to_idx)
                if self.is_valid_action(action):
                    actions.append(action)
        
        return actions
    
    def is_goal(self) -> bool:
        """
        この状態がゴール状態かどうかを判定する
        すべてのチューブが同じ色のみで満たされているか、空であれば完了
        
        Returns:
            ゴール状態ならTrue、そうでなければFalse
        """
        for tube in self.tubes:
            # 空のチューブはOK
            if not tube:
                continue
                
            # チューブに異なる色がある場合はゴールでない
            if len(set(tube)) > 1:
                return False
                
            # チューブが満杯でないか、もしくは全て同じ色でない場合はゴールでない
            if len(tube) < self.max_tube_capacity and len(tube) > 0:
                return False
        
        return True
    
    def apply_action(self, action: Action) -> 'State':
        """
        アクションを適用して新しい状態を生成する
        
        Args:
            action: 適用するアクション
            
        Returns:
            新しい状態
        """
        if not isinstance(action, WSPAction):
            raise ValueError("アクションはWSPActionのインスタンスである必要があります")
        
        if not self.is_valid_action(action):
            raise ValueError("無効なアクションです")
            
        # 状態のディープコピーを作成
        new_tubes = deepcopy(self.tubes)
        
        # 移動元と移動先のチューブを取得
        from_idx, to_idx = action.from_tube, action.to_tube
        from_tube = new_tubes[from_idx]
        to_tube = new_tubes[to_idx]
        
        # 移動元の上部にある同じ色のブロック数を計算
        top_color = from_tube[-1]
        count = 0
        for i in range(len(from_tube) - 1, -1, -1):
            if from_tube[i] == top_color:
                count += 1
            else:
                break
        
        # 移動先に入れられる量を計算
        available_space = self.max_tube_capacity - len(to_tube)
        move_amount = min(count, available_space)
        
        # 水を移動
        for _ in range(move_amount):
            to_tube.append(from_tube.pop())
        
        return WSPState(new_tubes, self.max_tube_capacity)
    
    def is_valid_action(self, action: Action) -> bool:
        """
        アクションが指定された状態で有効かどうかを判定する
        
        Args:
            action: 判定対象のアクション
            
        Returns:
            アクションが有効ならTrue、そうでなければFalse
        """
        if not isinstance(action, WSPAction):
            return False
            
        from_idx, to_idx = action.from_tube, action.to_tube
        
        # インデックスが範囲外の場合
        if from_idx < 0 or from_idx >= len(self.tubes) or to_idx < 0 or to_idx >= len(self.tubes):
            return False
            
        from_tube = self.tubes[from_idx]
        to_tube = self.tubes[to_idx]
        
        # 移動元のチューブが空の場合
        if not from_tube:
            return False
            
        # 移動先のチューブが満杯の場合
        if len(to_tube) >= self.max_tube_capacity:
            return False
            
        # 移動先が空でなく、上部の色が移動元と異なる場合
        if to_tube and to_tube[-1] != from_tube[-1]:
            return False
            
        return True
    
    def __str__(self) -> str:
        """
        状態の文字列表現を返す
        
        Returns:
            状態の文字列表現
        """
        result = []
        for i, tube in enumerate(self.tubes):
            tube_str = ','.join(tube) if tube else "空"
            result.append(f"チューブ{i}: [{tube_str}]")
        return '\n'.join(result)
    
    def __eq__(self, other: object) -> bool:
        """
        2つの状態が等しいかどうかを判定する
        
        Args:
            other: 比較対象のオブジェクト
            
        Returns:
            等しければTrue、そうでなければFalse
        """
        if not isinstance(other, WSPState):
            return False
            
        if len(self.tubes) != len(other.tubes):
            return False
            
        # チューブをソートして比較（チューブの順序は状態に影響しない）
        sorted_self = sorted([tuple(tube) for tube in self.tubes])
        sorted_other = sorted([tuple(tube) for tube in other.tubes])
        
        return sorted_self == sorted_other
    
    def __hash__(self) -> int:
        """
        状態のハッシュ値を返す
        
        Returns:
            ハッシュ値
        """
        # チューブをソートしてハッシュ値を計算
        sorted_tubes = sorted([tuple(tube) for tube in self.tubes])
        return hash(tuple(sorted_tubes)) 