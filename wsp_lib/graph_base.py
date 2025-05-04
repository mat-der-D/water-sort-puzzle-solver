#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List, TypeVar


class Action(ABC):
    """
    アクションクラス（グラフのエッジに対応）
    状態間の遷移を表す抽象基底クラス
    """
    
    @abstractmethod
    def __str__(self) -> str:
        """
        アクションの文字列表現を返す
        
        Returns:
            アクションの文字列表現
        """
        pass
    
    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        2つのアクションが等しいかどうかを判定する
        
        Args:
            other: 比較対象のオブジェクト
            
        Returns:
            等しければTrue、そうでなければFalse
        """
        pass
    
    @abstractmethod
    def __hash__(self) -> int:
        """
        アクションのハッシュ値を返す
        
        Returns:
            ハッシュ値
        """
        pass


class State(ABC):
    """
    状態クラス（グラフのノードに対応）
    探索空間内の状態を表す抽象基底クラス
    """
    
    @abstractmethod
    def get_possible_actions(self) -> List[Action]:
        """
        この状態から実行可能なアクションのリストを返す
        
        Returns:
            実行可能なアクションのリスト
        """
        pass
    
    @abstractmethod
    def is_goal(self) -> bool:
        """
        この状態がゴール状態かどうかを判定する
        
        Returns:
            ゴール状態ならTrue、そうでなければFalse
        """
        pass
    
    @abstractmethod
    def apply_action(self, action: Action) -> 'State':
        """
        アクションを適用して新しい状態を生成する
        
        Args:
            action: 適用するアクション
            
        Returns:
            新しい状態
        """
        pass
    
    @abstractmethod
    def is_valid_action(self, action: Action) -> bool:
        """
        アクションが指定された状態で有効かどうかを判定する
        
        Args:
            action: 判定対象のアクション
            
        Returns:
            アクションが有効ならTrue、そうでなければFalse
        """
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """
        状態の文字列表現を返す
        
        Returns:
            状態の文字列表現
        """
        pass
    
    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        2つの状態が等しいかどうかを判定する
        
        Args:
            other: 比較対象のオブジェクト
            
        Returns:
            等しければTrue、そうでなければFalse
        """
        pass
    
    @abstractmethod
    def __hash__(self) -> int:
        """
        状態のハッシュ値を返す
        
        Returns:
            ハッシュ値
        """
        pass 