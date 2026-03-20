#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Direction, Hat, Stick
from Commands.PythonCommandBase import ImageProcPythonCommand
import enum
import time
import requests
import sys
import win32gui,win32con
import json
import os
#from Keys import Touchscreen
#from SerialController.Commands.Keys import Touchscreen # pywin32
######################################################
#
# ZA_story
# ベースとなる機能ライブラリクラス
# これを継承し、組み合わせて実際のコマンドを作る
#
######################################################
class ZA_story_Base(ImageProcPythonCommand):    
    def __init__(self, cam):
        super().__init__(cam)
        self.isDebug = True
        self.showNoMatchTemplate = True
        self.showTemplateMatchVal = False
        self.commandWaitTime = 0.02
        self.frameWaitTime = 1.0/30.0
        self.testcode=0
        self.show_value_bool = False
        
        self.chapter_major=0
        self.chapter_minor=0
        
        self.check_picture=0
        self.TESTADDCODE=0
        self.ZL_state = 0

        # ポケモン選択間隔 ,マップ選択間隔 ,ZL間隔 ,バトルゾーン判断開始までの猶予期間 ,RIGHT_Stick間隔
        #self.sleetimes = [0.25,0.2,0.01,0.4,0,13]

        self.STATE_MAIN_FUNCTION = {
            "MAIN_STATE_INIT": self.main_state_init,
            "MAIN_0_START": self.main_0_start,
            "MAIN_1_Z_LANK": self.main_1_z_lank,
            "MAIN_2_Y_V_LANK": self.main_2_y_v_lank,
            "MAIN_3_F_LANK": self.main_3_f_lank,
            "MAIN_4_E_LANK": self.main_4_e_lank,
            "MAIN_5_D_LANK": self.main_5_d_lank,
            "MAIN_6_C_LANK": self.main_6_c_lank,
            "MAIN_7_B_LANK": self.main_7_b_lank,
            "MAIN_8_STORY_LAST": self.main_8_story_last,
            "MAIN_STORY_END": self.main_story_end,
        }
        self.main_current_state="MAIN_STATE_INIT"
        #
        self.main_current_state_init="MAIN_1_Z_LANK" 
        self.main_current_state_init="MAIN_2_Y_V_LANK" 
        #self.main_current_state_init="MAIN_3_F_LANK"
        #self.main_current_state_init="MAIN_4_E_LANK"
        #self.main_current_state_init="MAIN_5_D_LANK"
        #self.main_current_state_init="MAIN_6_C_LANK"
        #self.main_current_state_init="MAIN_7_B_LANK"
        #self.main_current_state_init="MAIN_8_STORY_LAST"
        #self.main_current_state_init="" 
        
        self.STATE_1_STORY_FUNCTION = {
            "1_STORY_START_CHECK": self._1_story_start_check,
            "1_STORY_TRAIN_OUT": self._1_story_train_out,
            
            ## BKUP_START_POINT
            "1_STORY_STATION_OUT": self._1_story_staition_out,
            
            "1_STORY_STATION_FRONT": self._1_story_staition_front,
            "1_STORY_STATION_LEAVE_MOVE": self._1_story_staition_leave_move,
            "1_STORY_BAG_CHASE_END": self._1_story_bag_chase_end,
            "1_STORY_FARST_POKEMON_SELECT": self._1_story_farst_pokemon_select,
            "1_STORY_FARST_BATTLE": self._1_story_farst_battle,
            "1_STORY_FARST_BATTLE_END": self._1_story_farst_battle_end,
            "1_STORY_FARST_BATTLE_ZONE_MOVE1": self._1_story_farst_battle_zone_move1,
            "1_STORY_SECOND_BATTLE_START": self._1_story_second_battle_start,
            "1_STORY_SECOND_BATTLE": self._1_story_second_battle,
            "1_STORY_SECOND_BATTLE_END": self._1_story_second_battle_end,
            
            "1_STORY_FARST_BATTLE_ZONE_MOVE2": self._1_story_farst_battle_zone_move2,
            
            "1_STORY_FARST_MOVIE_END": self._1_story_farst_movie_end,
            "1_STORY_FARST_BATTLE_ZONE_MOVE3": self._1_story_farst_battle_zone_move3,
            "1_STORY_FARST_BATTLE_ZONE_OUT": self._1_story_farst_battle_zone_out,
            "1_STORY_FARST_BATTLE_ZONE_MOVE4": self._1_story_farst_battle_zone_move4,
            
            "1_STORY_HOTEL_Z_ARRIVAL": self._1_story_hote_z_arrival,
            "1_STORY_HOTEL_Z_MOVE1": self._1_story_hote_z_move1,
            "1_STORY_HOTEL_Z_MOVE2": self._1_story_hote_z_move2,
            "1_STORY_HOTEL_Z_FAST_IN": self._1_story_hote_z_fast_in,
            "1_STORY_HOTEL_Z_MOVE3": self._1_story_hote_z_move3,
            "1_STORY_AZ_CHAT": self._1_story_az_chat,
            "1_STORY_HOTEL_Z_MOVE4": self._1_story_hote_z_move4,
            
            "1_STORY_FAST_ELEVATOR": self._1_story_fast_elevator,
            "1_STORY_HOTEL_Z_MOVE5": self._1_story_hote_z_move5,
            "1_STORY_HOTEL_Z_MOVE6": self._1_story_hote_z_move6,
            "1_STORY_HOTEL_Z_MOVE7": self._1_story_hote_z_move7,
            "1_STORY_HOTEL_Z_MOVE8": self._1_story_hote_z_move8,
            "1_STORY_HOTEL_Z_MOVE9": self._1_story_hote_z_move9,
            "1_STORY_HOTEL_Z_MOVE10": self._1_story_hote_z_move10,
            "1_STORY_HOTEL_Z_MOVE11": self._1_story_hote_z_move11,
            "1_STORY_HOTEL_Z_MOVE12": self._1_story_hote_z_move12,
            "1_STORY_HOTEL_Z_MOVE13": self._1_story_hote_z_move13,
            "1_STORY_HOTEL_Z_MOVE14": self._1_story_hote_z_move14,
            "1_STORY_HOTEL_Z_MOVE15": self._1_story_hote_z_move15,
            
            "1_STORY_THIRD_BATTLE": self._1_story_third_battle,
            "1_STORY_THIRD_BATTLE_END": self._1_story_third_battle_end,
            
            "1_STORY_OUT_HOTEL_Z_1": self._1_story_out_hotel_z_1,
            "1_STORY_OUT_HOTEL_Z_2": self._1_story_out_hotel_z_2,
            "1_STORY_OUT_HOTEL_Z_3": self._1_story_out_hotel_z_3,
            "1_STORY_OUT_HOTEL_Z_4": self._1_story_out_hotel_z_4,
            "1_STORY_OUT_HOTEL_Z_5": self._1_story_out_hotel_z_5,
            "1_STORY_OUT_HOTEL_Z_6": self._1_story_out_hotel_z_6,
            "1_STORY_OUT_HOTEL_Z_7": self._1_story_out_hotel_z_7,
            "1_STORY_OUT_HOTEL_Z_8": self._1_story_out_hotel_z_8,
            "1_STORY_OUT_HOTEL_Z_9": self._1_story_out_hotel_z_9,
            
            "1_STORY_WANINOKO_SKILL_CHANGE1": self._1_story_waninoko_skill_change1,
            "1_STORY_WANINOKO_SKILL_CHANGE2": self._1_story_waninoko_skill_change2,
            
            "1_STORY_OUT_HOTEL_Z_10": self._1_story_out_hotel_z_10,
            "1_STORY_OUT_HOTEL_Z_11": self._1_story_out_hotel_z_11,
            "1_STORY_OUT_HOTEL_Z_12": self._1_story_out_hotel_z_12,
            "1_STORY_OUT_HOTEL_Z_13": self._1_story_out_hotel_z_13,
            "1_STORY_OUT_HOTEL_Z_14": self._1_story_out_hotel_z_14,
            "1_STORY_OUT_HOTEL_Z_15": self._1_story_out_hotel_z_15,
            "1_STORY_OUT_HOTEL_Z_16": self._1_story_out_hotel_z_16,    
            "1_STORY_OUT_HOTEL_Z_17": self._1_story_out_hotel_z_17,
            "1_STORY_OUT_HOTEL_Z_18": self._1_story_out_hotel_z_18,
            
            "1_STORY_OUT_HOTEL_Z_18_1": self._1_story_out_hotel_z_18_1,
            "1_STORY_OUT_HOTEL_Z_18_2": self._1_story_out_hotel_z_18_2,
            
            "1_STORY_OUT_HOTEL_Z_19": self._1_story_out_hotel_z_19,
            "1_STORY_OUT_HOTEL_Z_19_1": self._1_story_out_hotel_z_19_1,
            
            "1_STORY_OUT_HOTEL_Z_20": self._1_story_out_hotel_z_20,
            "1_STORY_OUT_HOTEL_Z_20_1": self._1_story_out_hotel_z_20_1,
            "1_STORY_OUT_HOTEL_Z_21": self._1_story_out_hotel_z_21,
            "1_STORY_OUT_HOTEL_Z_22": self._1_story_out_hotel_z_22,
            "1_STORY_OUT_HOTEL_Z_23": self._1_story_out_hotel_z_23,
            "1_STORY_OUT_HOTEL_Z_24": self._1_story_out_hotel_z_24,
            "1_STORY_OUT_HOTEL_Z_25": self._1_story_out_hotel_z_25,
            "1_STORY_OUT_HOTEL_Z_26": self._1_story_out_hotel_z_26,
            "1_STORY_OUT_HOTEL_Z_27": self._1_story_out_hotel_z_27,
            "1_STORY_OUT_HOTEL_Z_28": self._1_story_out_hotel_z_28,
            "1_STORY_OUT_HOTEL_Z_29": self._1_story_out_hotel_z_29,
            "1_STORY_OUT_HOTEL_Z_30": self._1_story_out_hotel_z_30,
            "1_STORY_OUT_HOTEL_Z_31": self._1_story_out_hotel_z_31,
            "1_STORY_OUT_HOTEL_Z_32": self._1_story_out_hotel_z_32,
            "1_STORY_OUT_HOTEL_Z_33": self._1_story_out_hotel_z_33,
            "1_STORY_OUT_HOTEL_Z_34": self._1_story_out_hotel_z_34,
            "1_STORY_OUT_HOTEL_Z_35": self._1_story_out_hotel_z_35,
            
            "1_STORY_OUT_HOTEL_Z_35": self._1_story_out_hotel_z_35,
            "1_STORY_OUT_HOTEL_Z_36": self._1_story_out_hotel_z_36,
            "1_STORY_OUT_HOTEL_Z_37": self._1_story_out_hotel_z_37,
            "1_STORY_OUT_HOTEL_Z_38": self._1_story_out_hotel_z_38,
            
            "1_STORY_WANINOKO_SKILL_CHANGE3": self._1_story_waninoko_skill_change3,
            "1_STORY_WANINOKO_SKILL_CHANGE4": self._1_story_waninoko_skill_change4,
            "1_STORY_WANINOKO_SKILL_CHANGE5": self._1_story_waninoko_skill_change5,
            "1_STORY_WANINOKO_SKILL_CHANGE6": self._1_story_waninoko_skill_change6,
            "1_STORY_WANINOKO_SKILL_CHANGE7": self._1_story_waninoko_skill_change7,
            "1_STORY_WANINOKO_SKILL_CHANGE8": self._1_story_waninoko_skill_change8,
            "1_STORY_WANINOKO_SKILL_CHANGE9": self._1_story_waninoko_skill_change9,
            
            "1_STORY_OUT_HOTEL_Z_39_0": self._1_story_out_hotel_z_39_0,
            "1_STORY_OUT_HOTEL_Z_39": self._1_story_out_hotel_z_39,
            "1_STORY_OUT_HOTEL_Z_39_1": self._1_story_out_hotel_z_39_1,
            
            "1_STORY_OUT_HOTEL_Z_40": self._1_story_out_hotel_z_40,
            "1_STORY_OUT_HOTEL_Z_40_1": self._1_story_out_hotel_z_40_1,
            
            "1_STORY_OUT_HOTEL_Z_41": self._1_story_out_hotel_z_41,
            "1_STORY_OUT_HOTEL_Z_42": self._1_story_out_hotel_z_42,
            "1_STORY_OUT_HOTEL_Z_43": self._1_story_out_hotel_z_43,
            "1_STORY_OUT_HOTEL_Z_44": self._1_story_out_hotel_z_44,
            "1_STORY_OUT_HOTEL_Z_45": self._1_story_out_hotel_z_45,
            "1_STORY_OUT_HOTEL_Z_46": self._1_story_out_hotel_z_46,
            "1_STORY_OUT_HOTEL_Z_47": self._1_story_out_hotel_z_47,
            "1_STORY_OUT_HOTEL_Z_48": self._1_story_out_hotel_z_48,
            "1_STORY_OUT_HOTEL_Z_49": self._1_story_out_hotel_z_49,
            "1_STORY_OUT_HOTEL_Z_50": self._1_story_out_hotel_z_50,
            "1_STORY_OUT_HOTEL_Z_51": self._1_story_out_hotel_z_51,
            "1_STORY_OUT_HOTEL_Z_52": self._1_story_out_hotel_z_52,
            "1_STORY_OUT_HOTEL_Z_53": self._1_story_out_hotel_z_53,
            "1_STORY_OUT_HOTEL_Z_54": self._1_story_out_hotel_z_54,
            "1_STORY_OUT_HOTEL_Z_55": self._1_story_out_hotel_z_55,
            "1_STORY_OUT_HOTEL_Z_56": self._1_story_out_hotel_z_56,
            "1_STORY_OUT_HOTEL_Z_57": self._1_story_out_hotel_z_57,
            "1_STORY_OUT_HOTEL_Z_58": self._1_story_out_hotel_z_58,
            "1_STORY_OUT_HOTEL_Z_59": self._1_story_out_hotel_z_59,
            "1_STORY_OUT_HOTEL_Z_60": self._1_story_out_hotel_z_60,
            "1_STORY_OUT_HOTEL_Z_60_1": self._1_story_out_hotel_z_60_1,
            "1_STORY_OUT_HOTEL_Z_60_2": self._1_story_out_hotel_z_60_2,
            
            "1_STORY_OUT_HOTEL_Z_61": self._1_story_out_hotel_z_61,
            "1_STORY_OUT_HOTEL_Z_62": self._1_story_out_hotel_z_62,
            "1_STORY_OUT_HOTEL_Z_63": self._1_story_out_hotel_z_63,
            "1_STORY_OUT_HOTEL_Z_64": self._1_story_out_hotel_z_64,
            "1_STORY_OUT_HOTEL_Z_65": self._1_story_out_hotel_z_65,
            "1_STORY_OUT_HOTEL_Z_66": self._1_story_out_hotel_z_66,
            "1_STORY_OUT_HOTEL_Z_67": self._1_story_out_hotel_z_67,
            "1_STORY_OUT_HOTEL_Z_68": self._1_story_out_hotel_z_68,
            "1_STORY_OUT_HOTEL_Z_69": self._1_story_out_hotel_z_69,
            "1_STORY_OUT_HOTEL_Z_70": self._1_story_out_hotel_z_70,
            "1_STORY_OUT_HOTEL_Z_71": self._1_story_out_hotel_z_71,
            "1_STORY_OUT_HOTEL_Z_72": self._1_story_out_hotel_z_72,
            "1_STORY_OUT_HOTEL_Z_73": self._1_story_out_hotel_z_73,
            "1_STORY_OUT_HOTEL_Z_74": self._1_story_out_hotel_z_74,
            "1_STORY_OUT_HOTEL_Z_75": self._1_story_out_hotel_z_75,
            "1_STORY_OUT_HOTEL_Z_76": self._1_story_out_hotel_z_76,
            "1_STORY_OUT_HOTEL_Z_77": self._1_story_out_hotel_z_77,
            "1_STORY_OUT_HOTEL_Z_78": self._1_story_out_hotel_z_78,
            "1_STORY_OUT_HOTEL_Z_79": self._1_story_out_hotel_z_79,
            "1_STORY_OUT_HOTEL_Z_80": self._1_story_out_hotel_z_80,
            "1_STORY_OUT_HOTEL_Z_81": self._1_story_out_hotel_z_81,
            "1_STORY_OUT_HOTEL_Z_82": self._1_story_out_hotel_z_82,
            "1_STORY_OUT_HOTEL_Z_83": self._1_story_out_hotel_z_83,
            "1_STORY_OUT_HOTEL_Z_84": self._1_story_out_hotel_z_84,
            "1_STORY_OUT_HOTEL_Z_85": self._1_story_out_hotel_z_85,
            "1_STORY_END": self._1_story_end,
        }
        self._1_story_current_state="1_STORY_START_CHECK" 
        self._1_story_current_state_init="2_STORY_X_LANK_MOVE9"
        #self._1_story_current_state_init="" 
        self._1_story_2nd_get_comment=0
        
        self._1_story_out_hotel_z_20_not_eyecheck_count=0
        
        self.STATE_2_STORY_FUNCTION = {
            "2_STORY_START_CHECK": self._2_story_start_check,
            "2_STORY_TOWER_1": self._2_story_tower_1,
            "2_STORY_TOWER_2": self._2_story_tower_2,
            "2_STORY_TOWER_3": self._2_story_tower_3,
            "2_STORY_TOWER_4": self._2_story_tower_4,
            "2_STORY_TOWER_5": self._2_story_tower_5,
            "2_STORY_TOWER_6": self._2_story_tower_6,
            "2_STORY_TOWER_7": self._2_story_tower_7,
            "2_STORY_TOWER_8": self._2_story_tower_8,
            "2_STORY_TOWER_9": self._2_story_tower_9,
            "2_STORY_TOWER_10": self._2_story_tower_10,
            "2_STORY_TOWER_11": self._2_story_tower_11,
            "2_STORY_TOWER_12": self._2_story_tower_12,
            "2_STORY_TOWER_13": self._2_story_tower_13,
            "2_STORY_TOWER_14": self._2_story_tower_14,
            "2_STORY_TOWER_15_0": self._2_story_tower_15_0,
            "2_STORY_TOWER_15": self._2_story_tower_15,
            "2_STORY_TOWER_16": self._2_story_tower_16,
            "2_STORY_TOWER_17": self._2_story_tower_17,
            "2_STORY_TOWER_18": self._2_story_tower_18,
            "2_STORY_TOWER_19": self._2_story_tower_19,
            "2_STORY_TOWER_20": self._2_story_tower_20,
            "2_STORY_TOWER_21": self._2_story_tower_21,
            "2_STORY_TOWER_22": self._2_story_tower_22,
            "2_STORY_TOWER_23": self._2_story_tower_23,
            "2_STORY_TOWER_24": self._2_story_tower_24,
            "2_STORY_TOWER_25": self._2_story_tower_25,
            "2_STORY_TOWER_26": self._2_story_tower_26,
            "2_STORY_TOWER_27": self._2_story_tower_27,
            "2_STORY_TOWER_28": self._2_story_tower_28,
            "2_STORY_TOWER_29": self._2_story_tower_29,
            "2_STORY_TOWER_30": self._2_story_tower_30,
            "2_STORY_TOWER_31": self._2_story_tower_31,
            "2_STORY_TOWER_32": self._2_story_tower_32,
            "2_STORY_TOWER_33": self._2_story_tower_33,
            "2_STORY_TOWER_34": self._2_story_tower_34,
            "2_STORY_TOWER_35": self._2_story_tower_35,
            "2_STORY_TOWER_36": self._2_story_tower_36,
            "2_STORY_TOWER_37": self._2_story_tower_37,
            "2_STORY_TOWER_38": self._2_story_tower_38,
            "2_STORY_TOWER_39": self._2_story_tower_39,
            "2_STORY_TOWER_40": self._2_story_tower_40,
            "2_STORY_TOWER_41": self._2_story_tower_41,
            "2_STORY_TOWER_42": self._2_story_tower_42,
            "2_STORY_TOWER_43": self._2_story_tower_43,
            "2_STORY_TOWER_44": self._2_story_tower_44,
            "2_STORY_TOWER_45": self._2_story_tower_45,
            "2_STORY_TOWER_46": self._2_story_tower_46,
            
            "2_STORY_MAPPING_1": self._2_story_mapping_1,
            "2_STORY_MAPPING_2": self._2_story_mapping_2,
            "2_STORY_MAPPING_3": self._2_story_mapping_3,         
            "2_STORY_MAPPING_4": self._2_story_mapping_4,         
            "2_STORY_MAPPING_5": self._2_story_mapping_5,         
            "2_STORY_MAPPING_6": self._2_story_mapping_6,         
            "2_STORY_MAPPING_7": self._2_story_mapping_7,         
            "2_STORY_MAPPING_8": self._2_story_mapping_8,         
            "2_STORY_MAPPING_9": self._2_story_mapping_9,         
            "2_STORY_MAPPING_10": self._2_story_mapping_10,         
            "2_STORY_MAPPING_11": self._2_story_mapping_11,         
            "2_STORY_MAPPING_12": self._2_story_mapping_12,         
            "2_STORY_MAPPING_13": self._2_story_mapping_13,          
            "2_STORY_MAPPING_14": self._2_story_mapping_14,         
            "2_STORY_MAPPING_15": self._2_story_mapping_15,          
            "2_STORY_MAPPING_16": self._2_story_mapping_16,         
            "2_STORY_MAPPING_17": self._2_story_mapping_17,          
            "2_STORY_MAPPING_18": self._2_story_mapping_18,         
            "2_STORY_MAPPING_19": self._2_story_mapping_19,          
            "2_STORY_MAPPING_20": self._2_story_mapping_20,            
            "2_STORY_MAPPING_21": self._2_story_mapping_21,          
            "2_STORY_MAPPING_22": self._2_story_mapping_22,          
            "2_STORY_MAPPING_23": self._2_story_mapping_23,          
            "2_STORY_MAPPING_24": self._2_story_mapping_24,          
            "2_STORY_MAPPING_25": self._2_story_mapping_25,          
            "2_STORY_MAPPING_26": self._2_story_mapping_26,          
            "2_STORY_MAPPING_27": self._2_story_mapping_27,          
            "2_STORY_MAPPING_28": self._2_story_mapping_28,          
            "2_STORY_MAPPING_29": self._2_story_mapping_29,          
            "2_STORY_MAPPING_30": self._2_story_mapping_30,          
            "2_STORY_MAPPING_31": self._2_story_mapping_31,          
            "2_STORY_MAPPING_32": self._2_story_mapping_32,           
            "2_STORY_MAPPING_33": self._2_story_mapping_33,           
            "2_STORY_MAPPING_34": self._2_story_mapping_34,           
            "2_STORY_MAPPING_35": self._2_story_mapping_35,           
            "2_STORY_MAPPING_36": self._2_story_mapping_36,           
            "2_STORY_MAPPING_37": self._2_story_mapping_37,           
            "2_STORY_MAPPING_38": self._2_story_mapping_38,           
            "2_STORY_MAPPING_39": self._2_story_mapping_39,           
            "2_STORY_MAPPING_40": self._2_story_mapping_40,           
            "2_STORY_MAPPING_41": self._2_story_mapping_41,           
            "2_STORY_MAPPING_42": self._2_story_mapping_42,           
            "2_STORY_MAPPING_43": self._2_story_mapping_43,             
            "2_STORY_MAPPING_44": self._2_story_mapping_44,           
            "2_STORY_MAPPING_45": self._2_story_mapping_45,
                         
            "2_STORY_MAPPING_46": self._2_story_mapping_46, 
            "2_STORY_MAPPING_47": self._2_story_mapping_47, 
            "2_STORY_MAPPING_48": self._2_story_mapping_48, 
            "2_STORY_MAPPING_49": self._2_story_mapping_49, 
            "2_STORY_MAPPING_50": self._2_story_mapping_50, 
            "2_STORY_MAPPING_51": self._2_story_mapping_51, 
            "2_STORY_MAPPING_52": self._2_story_mapping_52, 
            "2_STORY_MAPPING_53": self._2_story_mapping_53, 
            "2_STORY_MAPPING_54": self._2_story_mapping_54, 
            "2_STORY_MAPPING_55": self._2_story_mapping_55, 
            "2_STORY_MAPPING_56": self._2_story_mapping_56, 
            "2_STORY_MAPPING_57": self._2_story_mapping_57, 
            "2_STORY_MAPPING_58": self._2_story_mapping_58, 
            "2_STORY_MAPPING_59": self._2_story_mapping_59, 
            "2_STORY_MAPPING_60": self._2_story_mapping_60, 
            "2_STORY_MAPPING_61": self._2_story_mapping_61,  
            "2_STORY_MAPPING_62": self._2_story_mapping_62, 
            "2_STORY_MAPPING_63": self._2_story_mapping_63, 
            "2_STORY_MAPPING_64": self._2_story_mapping_64, 
            "2_STORY_MAPPING_65": self._2_story_mapping_65,
            "2_STORY_MAPPING_66": self._2_story_mapping_66, 
            "2_STORY_MAPPING_67": self._2_story_mapping_67, 
            "2_STORY_MAPPING_68": self._2_story_mapping_68, 
            "2_STORY_MAPPING_69": self._2_story_mapping_69, 
            "2_STORY_MAPPING_70": self._2_story_mapping_70, 
            "2_STORY_MAPPING_71": self._2_story_mapping_71,  
            "2_STORY_MAPPING_72": self._2_story_mapping_72,  
            "2_STORY_MAPPING_73": self._2_story_mapping_73,  
            "2_STORY_MAPPING_74": self._2_story_mapping_74,  
            "2_STORY_MAPPING_75": self._2_story_mapping_75,  
            "2_STORY_MAPPING_76": self._2_story_mapping_76,  
            "2_STORY_MAPPING_77": self._2_story_mapping_77,  
            "2_STORY_MAPPING_78": self._2_story_mapping_78,  
            "2_STORY_MAPPING_79": self._2_story_mapping_79,  
            "2_STORY_MAPPING_80": self._2_story_mapping_80,  
            "2_STORY_MAPPING_81_0": self._2_story_mapping_81_0,  
            "2_STORY_MAPPING_81": self._2_story_mapping_81,   
            "2_STORY_MAPPING_82": self._2_story_mapping_82,   
            "2_STORY_MAPPING_83": self._2_story_mapping_83,   
            "2_STORY_MAPPING_84": self._2_story_mapping_84,   
            "2_STORY_MAPPING_85": self._2_story_mapping_85,   
            "2_STORY_MAPPING_86": self._2_story_mapping_86,   
            "2_STORY_MAPPING_87": self._2_story_mapping_87,   
            "2_STORY_MAPPING_88": self._2_story_mapping_88,   
            "2_STORY_MAPPING_89": self._2_story_mapping_89,   
            "2_STORY_MAPPING_90": self._2_story_mapping_90,   
            "2_STORY_MAPPING_91": self._2_story_mapping_91,   
            "2_STORY_MAPPING_92": self._2_story_mapping_92,   
            "2_STORY_MAPPING_93": self._2_story_mapping_93,   
            "2_STORY_MAPPING_94": self._2_story_mapping_94,   
            "2_STORY_MAPPING_95": self._2_story_mapping_95,   
            "2_STORY_MAPPING_96": self._2_story_mapping_96,   
            "2_STORY_MAPPING_97": self._2_story_mapping_97,   
            "2_STORY_MAPPING_98": self._2_story_mapping_98,   
            "2_STORY_MAPPING_99": self._2_story_mapping_99,   
            "2_STORY_MAPPING_100": self._2_story_mapping_100,   
            "2_STORY_MAPPING_101": self._2_story_mapping_101,   
            "2_STORY_MAPPING_102": self._2_story_mapping_102,   
            "2_STORY_MAPPING_103": self._2_story_mapping_103,   
            "2_STORY_MAPPING_104": self._2_story_mapping_104,   
            "2_STORY_MAPPING_105": self._2_story_mapping_105,   
            "2_STORY_MAPPING_106": self._2_story_mapping_106,   
            "2_STORY_MAPPING_107": self._2_story_mapping_107,   
            "2_STORY_MAPPING_108": self._2_story_mapping_108,   
            "2_STORY_MAPPING_109": self._2_story_mapping_109,       

            "2_STORY_TOWER_47": self._2_story_tower_47,
            "2_STORY_TOWER_48": self._2_story_tower_48,
            "2_STORY_TOWER_49": self._2_story_tower_49,
            "2_STORY_TOWER_50": self._2_story_tower_50,
            "2_STORY_TOWER_51": self._2_story_tower_51,
            "2_STORY_TOWER_52": self._2_story_tower_52,
            "2_STORY_TOWER_53": self._2_story_tower_53,
            "2_STORY_TOWER_54": self._2_story_tower_54,
            "2_STORY_TOWER_55": self._2_story_tower_55,
            "2_STORY_TOWER_56": self._2_story_tower_56,
            "2_STORY_TOWER_57": self._2_story_tower_57,
            "2_STORY_TOWER_58": self._2_story_tower_58,
            "2_STORY_TOWER_59": self._2_story_tower_59,
            "2_STORY_TOWER_60": self._2_story_tower_60,
            "2_STORY_TOWER_61": self._2_story_tower_61,
            "2_STORY_TOWER_62": self._2_story_tower_62,
            "2_STORY_TOWER_63": self._2_story_tower_63,
            "2_STORY_TOWER_64": self._2_story_tower_64,
            "2_STORY_TOWER_65": self._2_story_tower_65,
            "2_STORY_TOWER_66": self._2_story_tower_66,
            "2_STORY_TOWER_67": self._2_story_tower_67,
            "2_STORY_TOWER_68": self._2_story_tower_68,
            "2_STORY_TOWER_69": self._2_story_tower_69,
            "2_STORY_TOWER_70": self._2_story_tower_70,
            "2_STORY_TOWER_71": self._2_story_tower_71,
            "2_STORY_TOWER_72": self._2_story_tower_72,
            "2_STORY_TOWER_73": self._2_story_tower_73,
            "2_STORY_TOWER_74": self._2_story_tower_74,
            "2_STORY_TOWER_75": self._2_story_tower_75,
            "2_STORY_TOWER_76": self._2_story_tower_76,
            "2_STORY_TOWER_77": self._2_story_tower_77,
            "2_STORY_TOWER_78": self._2_story_tower_78,
            "2_STORY_TOWER_79": self._2_story_tower_79,
            "2_STORY_TOWER_80": self._2_story_tower_80,
            "2_STORY_TOWER_81": self._2_story_tower_81,
            "2_STORY_TOWER_82": self._2_story_tower_82,
            "2_STORY_TOWER_83": self._2_story_tower_83,
            "2_STORY_TOWER_84": self._2_story_tower_84,

            "2_STORY_Y_LANK_BATTLE_ZONE": self._2_story_y_lank_battle_zone,
            
            "2_STORY_Y_LANK_MOVE0": self._2_story_y_lank_move0,
            "2_STORY_Y_LANK_MOVE1": self._2_story_y_lank_move1,
            "2_STORY_Y_LANK_MOVE2": self._2_story_y_lank_move2,
            "2_STORY_Y_LANK_MOVE3": self._2_story_y_lank_move3,
            "2_STORY_Y_LANK_MOVE4": self._2_story_y_lank_move4,
            "2_STORY_Y_LANK_MOVE5": self._2_story_y_lank_move5,

            "2_STORY_Y_END":self._2_story_y_end,

            "2_STORY_X_LANK_MOVE1": self._2_story_x_lank_move1,
            "2_STORY_X_LANK_MOVE2": self._2_story_x_lank_move2,
            "2_STORY_X_LANK_MOVE3": self._2_story_x_lank_move3,
            "2_STORY_X_LANK_MOVE4": self._2_story_x_lank_move4,
            "2_STORY_X_LANK_MOVE5": self._2_story_x_lank_move5,
            "2_STORY_X_LANK_MOVE6": self._2_story_x_lank_move6,
            "2_STORY_X_LANK_MOVE7": self._2_story_x_lank_move7,
            "2_STORY_X_LANK_MOVE8": self._2_story_x_lank_move8,

            "2_STORY_X_LANK_BATTLE_ZONE": self._2_story_x_lank_battle_zone,

            "2_STORY_X_LANK_MOVE9": self._2_story_x_lank_move9,
            "2_STORY_X_LANK_MOVE10": self._2_story_x_lank_move10,
            "2_STORY_X_LANK_MOVE11": self._2_story_x_lank_move11,
            "2_STORY_X_LANK_MOVE12": self._2_story_x_lank_move12,
            "2_STORY_X_LANK_MOVE13": self._2_story_x_lank_move13,
            
            "2_STORY_W_LANK_MOVE1": self._2_story_w_lank_move1,
            "2_STORY_W_LANK_MOVE2": self._2_story_w_lank_move2,
            "2_STORY_W_LANK_MOVE3": self._2_story_w_lank_move3,
            "2_STORY_W_LANK_MOVE4": self._2_story_w_lank_move4,
            "2_STORY_W_LANK_MOVE5": self._2_story_w_lank_move5,
            "2_STORY_W_LANK_MOVE6": self._2_story_w_lank_move6,
            "2_STORY_W_LANK_MOVE7": self._2_story_w_lank_move7,
            
            "2_STORY_W_LANK_BATTLE_ZONE":self._2_story_w_lank_battle_zone,
            
            "2_STORY_W_LANK_MOVE8": self._2_story_w_lank_move8,
            "2_STORY_W_LANK_MOVE9": self._2_story_w_lank_move9,
            "2_STORY_W_LANK_MOVE10": self._2_story_w_lank_move10,
            "2_STORY_W_LANK_MOVE11": self._2_story_w_lank_move11,
            "2_STORY_W_LANK_MOVE12": self._2_story_w_lank_move12,
            "2_STORY_W_LANK_MOVE13": self._2_story_w_lank_move13,
            
            "2_STORY_ABSOL_MOVE1": self._2_story_absol_move1,
            "2_STORY_ABSOL_MOVE2": self._2_story_absol_move2,
            
            "2_STORY_ABSOL_BATTLE": self._2_story_absol_battle,
            
            "2_STORY_ABSOL_MOVE3": self._2_story_absol_move3,
            "2_STORY_ABSOL_MOVE4": self._2_story_absol_move4,
            
            "2_STORY_BOX_CHANGE1": self._2_story_box_change1,
            "2_STORY_BOX_CHANGE2": self._2_story_box_change2,
            "2_STORY_ITEM_GIVE1": self._2_story_item_give1,
            
            "2_STORY_ABSOL_MOVE5": self._2_story_absol_move5,
            "2_STORY_ABSOL_MOVE6": self._2_story_absol_move6,
            "2_STORY_ABSOL_MOVE7": self._2_story_absol_move7,
            "2_STORY_ABSOL_MOVE8": self._2_story_absol_move8,
            
               
            "2_STORY_MAPPING_110": self._2_story_mapping_110,
            "2_STORY_MAPPING_111": self._2_story_mapping_111,
            "2_STORY_MAPPING_112": self._2_story_mapping_112,
            "2_STORY_MAPPING_113": self._2_story_mapping_113, 
            "2_STORY_MAPPING_114_0": self._2_story_mapping_114_0,
            "2_STORY_MAPPING_114": self._2_story_mapping_114,
            "2_STORY_MAPPING_114_1": self._2_story_mapping_114_1,
            "2_STORY_MAPPING_115": self._2_story_mapping_115, 
            "2_STORY_MAPPING_116_0": self._2_story_mapping_116_0,
            "2_STORY_MAPPING_116": self._2_story_mapping_116,
            "2_STORY_MAPPING_116_1": self._2_story_mapping_116_1,
            "2_STORY_MAPPING_117": self._2_story_mapping_117,
            
            "2_STORY_ABSOL_MOVE9": self._2_story_absol_move9,
            
            "2_STORY_ABSOL_MOVE10": self._2_story_absol_move10,
            "2_STORY_ABSOL_MOVE11": self._2_story_absol_move11,
            "2_STORY_ABSOL_MOVE12": self._2_story_absol_move12,
            "2_STORY_ABSOL_MOVE13": self._2_story_absol_move13,
            "2_STORY_ABSOL_MOVE14": self._2_story_absol_move14,
            "2_STORY_ABSOL_MOVE15": self._2_story_absol_move15,
            "2_STORY_ABSOL_MOVE16": self._2_story_absol_move16,
            "2_STORY_ABSOL_MOVE17": self._2_story_absol_move17,
            "2_STORY_ABSOL_MOVE18": self._2_story_absol_move18,
            "2_STORY_ABSOL_MOVE19": self._2_story_absol_move19,
            "2_STORY_ABSOL_MOVE20": self._2_story_absol_move20,
            "2_STORY_ABSOL_MOVE21": self._2_story_absol_move21,
            "2_STORY_ABSOL_MOVE22": self._2_story_absol_move22,
            "2_STORY_ABSOL_MOVE23": self._2_story_absol_move23,
            "2_STORY_ABSOL_MOVE24": self._2_story_absol_move24,
            "2_STORY_ABSOL_MOVE25": self._2_story_absol_move25,
            "2_STORY_ABSOL_MOVE26": self._2_story_absol_move26,
            "2_STORY_ABSOL_MOVE27": self._2_story_absol_move27,
            "2_STORY_ABSOL_MOVE28": self._2_story_absol_move28,
            "2_STORY_ABSOL_MOVE29": self._2_story_absol_move29,
            "2_STORY_ABSOL_MOVE30": self._2_story_absol_move30,
            "2_STORY_ABSOL_MOVE31": self._2_story_absol_move31,
            "2_STORY_ABSOL_MOVE32": self._2_story_absol_move32,
            "2_STORY_ABSOL_MOVE33": self._2_story_absol_move33,
            "2_STORY_ABSOL_MOVE34": self._2_story_absol_move34,
            "2_STORY_ABSOL_MOVE35": self._2_story_absol_move35,
            "2_STORY_ABSOL_MOVE36": self._2_story_absol_move36,
            "2_STORY_ABSOL_MOVE37": self._2_story_absol_move37,
            "2_STORY_ABSOL_MOVE38": self._2_story_absol_move38,
            "2_STORY_RESTAURANT_DOHUTSU_LOOP": self._2_story_restaurant_dohutsu_loop,

            "2_STORY_MEGA_MOVE1": self._2_story_mega_move1,
            "2_STORY_MEGA_MOVE2": self._2_story_mega_move2,
            "2_STORY_MEGA_MOVE3": self._2_story_mega_move3,
            "2_STORY_MEGA_MOVE4": self._2_story_mega_move4,
            "2_STORY_MEGA_MOVE5": self._2_story_mega_move5,
            "2_STORY_MEGA_MOVE6": self._2_story_mega_move6,
            "2_STORY_MEGA_MOVE7": self._2_story_mega_move7,
            "2_STORY_MEGA_MOVE8": self._2_story_mega_move8,
            "2_STORY_MEGA_MOVE9": self._2_story_mega_move9,
            "2_STORY_MEGA_MOVE10": self._2_story_mega_move10,
            "2_STORY_MEGA_MOVE11": self._2_story_mega_move11,
            "2_STORY_MEGA_MOVE12": self._2_story_mega_move12,
            "2_STORY_MEGA_MOVE13": self._2_story_mega_move13,
            "2_STORY_MEGA_MOVE14": self._2_story_mega_move14,
            "2_STORY_MEGA_MOVE15": self._2_story_mega_move15,
            "2_STORY_MEGA_MOVE16": self._2_story_mega_move16,
            "2_STORY_MEGA_MOVE17": self._2_story_mega_move17,
            "2_STORY_MEGA_MOVE18": self._2_story_mega_move18,
            "2_STORY_MEGA_MOVE19": self._2_story_mega_move19,
            "2_STORY_MEGA_MOVE20": self._2_story_mega_move20,
            "2_STORY_MEGA_MOVE21": self._2_story_mega_move21,
            "2_STORY_MEGA_MOVE22": self._2_story_mega_move22,
            "2_STORY_MEGA_MOVE23": self._2_story_mega_move23,
            "2_STORY_MEGA_MOVE24": self._2_story_mega_move24,
            "2_STORY_MEGA_MOVE25": self._2_story_mega_move25,
            "2_STORY_MEGA_MOVE26": self._2_story_mega_move26,
            "2_STORY_MEGA_MOVE27": self._2_story_mega_move27,
            
            "2_STORY_END": self._2_story_end,


        }
        
        self._2_story_current_state="2_STORY_START_CHECK" 
        self._2_story_current_state_init= "2_STORY_ABSOL_MOVE1"

        self._2_story_restaurant_dohutsu_loop_count=0
        self._2_story_restaurant_dohutsu_loop_threshold=400
        
        self._2_story_restaurant_dohutsu_white_check=1
        self._2_story_restaurant_dohutsu_black_check=0
        
        self._2_story_restaurant_dohutsu_battle_count=0
        
        self.STATE_3_STORY_FUNCTION = {
            "3_STORY_START_CHECK": self._3_story_start_check,
            
            "3_STORY_CANARI_1": self._3_story_canari_1, 
            "3_STORY_CANARI_2": self._3_story_canari_2, 
            "3_STORY_CANARI_3": self._3_story_canari_3,  
            "3_STORY_CANARI_4": self._3_story_canari_4,  
            "3_STORY_CANARI_5": self._3_story_canari_5,  
            "3_STORY_CANARI_6": self._3_story_canari_6,  
            "3_STORY_CANARI_7": self._3_story_canari_7,  
            "3_STORY_CANARI_8": self._3_story_canari_8,  
            "3_STORY_CANARI_9": self._3_story_canari_9,  
            "3_STORY_CANARI_10": self._3_story_canari_10,  
            "3_STORY_CANARI_11": self._3_story_canari_11,   
            "3_STORY_CANARI_12": self._3_story_canari_12,   
            "3_STORY_CANARI_13": self._3_story_canari_13,   
            "3_STORY_CANARI_14": self._3_story_canari_14,   
            "3_STORY_CANARI_15": self._3_story_canari_15,   
            "3_STORY_CANARI_16": self._3_story_canari_16,   
            "3_STORY_CANARI_17": self._3_story_canari_17,   
            "3_STORY_CANARI_18": self._3_story_canari_18,   
            "3_STORY_CANARI_19": self._3_story_canari_19,   
            "3_STORY_CANARI_20": self._3_story_canari_20,    
            "3_STORY_CANARI_21": self._3_story_canari_21,   
            "3_STORY_CANARI_22": self._3_story_canari_22,   
            "3_STORY_CANARI_23": self._3_story_canari_23,   
            "3_STORY_CANARI_24": self._3_story_canari_24,   
            "3_STORY_CANARI_25": self._3_story_canari_25,   
            "3_STORY_CANARI_26": self._3_story_canari_26,   
            "3_STORY_CANARI_27": self._3_story_canari_27,   
            "3_STORY_CANARI_28": self._3_story_canari_28,   
            "3_STORY_CANARI_29": self._3_story_canari_29,   
            "3_STORY_CANARI_30": self._3_story_canari_30,   
            "3_STORY_CANARI_31": self._3_story_canari_31,    
            "3_STORY_CANARI_32": self._3_story_canari_32,    
            "3_STORY_CANARI_33": self._3_story_canari_33,    
            "3_STORY_CANARI_34": self._3_story_canari_34,    
            "3_STORY_CANARI_35": self._3_story_canari_35,    
            "3_STORY_CANARI_36": self._3_story_canari_36,    
            "3_STORY_CANARI_37": self._3_story_canari_37,    
            "3_STORY_CANARI_38": self._3_story_canari_38,    
            "3_STORY_CANARI_39": self._3_story_canari_39,   
            "3_STORY_CANARI_40": self._3_story_canari_40,    
            "3_STORY_CANARI_41": self._3_story_canari_41,   
            "3_STORY_CANARI_42": self._3_story_canari_42,   
            "3_STORY_CANARI_43": self._3_story_canari_43,   
            "3_STORY_CANARI_44": self._3_story_canari_44,   
            "3_STORY_CANARI_45": self._3_story_canari_45,   
            "3_STORY_CANARI_46": self._3_story_canari_46,   
            "3_STORY_CANARI_47": self._3_story_canari_47,   
            "3_STORY_CANARI_48": self._3_story_canari_48,   
            "3_STORY_CANARI_49": self._3_story_canari_49,   
            "3_STORY_CANARI_50": self._3_story_canari_50,   
            
            "3_STORY_MEGA_MOVE1": self._3_story_mega_move1, 
            "3_STORY_MEGA_MOVE2": self._3_story_mega_move2, 
            "3_STORY_MEGA_MOVE3": self._3_story_mega_move3, 
            "3_STORY_MEGA_MOVE4": self._3_story_mega_move4, 
            "3_STORY_MEGA_MOVE5": self._3_story_mega_move5, 
            "3_STORY_MEGA_MOVE6": self._3_story_mega_move6, 
            "3_STORY_MEGA_MOVE7": self._3_story_mega_move7, 
            "3_STORY_MEGA_MOVE8": self._3_story_mega_move8, 
            "3_STORY_MEGA_MOVE9": self._3_story_mega_move9,
            "3_STORY_MEGA_MOVE10": self._3_story_mega_move10,
            "3_STORY_MEGA_MOVE11": self._3_story_mega_move11, 
            "3_STORY_MEGA_MOVE12": self._3_story_mega_move12, 
            "3_STORY_MEGA_MOVE13": self._3_story_mega_move13, 
            "3_STORY_MEGA_MOVE14": self._3_story_mega_move14, 
            "3_STORY_MEGA_MOVE15": self._3_story_mega_move15, 
            "3_STORY_MEGA_MOVE16": self._3_story_mega_move16, 
            "3_STORY_MEGA_MOVE17": self._3_story_mega_move17, 
            "3_STORY_MEGA_MOVE18": self._3_story_mega_move18, 
            "3_STORY_MEGA_MOVE19": self._3_story_mega_move19, 
            "3_STORY_MEGA_MOVE20": self._3_story_mega_move20, 
            "3_STORY_MEGA_MOVE21": self._3_story_mega_move21,  
            "3_STORY_MEGA_MOVE22": self._3_story_mega_move22,  
            "3_STORY_MEGA_MOVE23": self._3_story_mega_move23,  
            "3_STORY_MEGA_MOVE24": self._3_story_mega_move24,  
            "3_STORY_MEGA_MOVE25": self._3_story_mega_move25,  
            "3_STORY_MEGA_MOVE26": self._3_story_mega_move26,  
            "3_STORY_MEGA_MOVE27": self._3_story_mega_move27,  
            "3_STORY_MEGA_MOVE28": self._3_story_mega_move28,  
            "3_STORY_MEGA_MOVE29": self._3_story_mega_move29,  
            "3_STORY_MEGA_MOVE30": self._3_story_mega_move30,  
             
             
            "3_STORY_END": self._3_story_end,
        }
        
        self._3_story_current_state="3_STORY_START_CHECK" 
        self._3_story_current_state_init= "3_STORY_END"

        self.STATE_4_STORY_FUNCTION = {
            "4_STORY_START_CHECK": self._4_story_start_check,
            
            "4_STORY_SHIRO_1": self._4_story_shiro_1,        
            "4_STORY_SHIRO_2": self._4_story_shiro_2,         
            "4_STORY_SHIRO_3": self._4_story_shiro_3,        
            "4_STORY_SHIRO_4": self._4_story_shiro_4,        
            "4_STORY_SHIRO_5": self._4_story_shiro_5,        
            "4_STORY_SHIRO_6": self._4_story_shiro_6,        
            "4_STORY_SHIRO_7": self._4_story_shiro_7,        
            "4_STORY_SHIRO_8": self._4_story_shiro_8,        
            "4_STORY_SHIRO_9": self._4_story_shiro_9,        
            "4_STORY_SHIRO_10": self._4_story_shiro_10,        
            "4_STORY_SHIRO_11": self._4_story_shiro_11,        
            "4_STORY_SHIRO_12": self._4_story_shiro_12,        
            "4_STORY_SHIRO_13": self._4_story_shiro_13,        
            "4_STORY_SHIRO_14": self._4_story_shiro_14,        
            "4_STORY_SHIRO_15": self._4_story_shiro_15,        
            "4_STORY_SHIRO_16": self._4_story_shiro_16,        
            "4_STORY_SHIRO_17": self._4_story_shiro_17,        
            "4_STORY_SHIRO_18": self._4_story_shiro_18,        
            "4_STORY_SHIRO_19": self._4_story_shiro_19,        
            "4_STORY_SHIRO_20": self._4_story_shiro_20,        
            "4_STORY_SHIRO_21": self._4_story_shiro_21,        
            "4_STORY_SHIRO_21_1": self._4_story_shiro_21_1,         
            "4_STORY_SHIRO_21_2": self._4_story_shiro_21_2,         
            "4_STORY_SHIRO_22": self._4_story_shiro_22,        
            "4_STORY_SHIRO_23": self._4_story_shiro_23,        
            "4_STORY_SHIRO_24": self._4_story_shiro_24,        
            "4_STORY_SHIRO_25": self._4_story_shiro_25,        
            "4_STORY_SHIRO_26": self._4_story_shiro_26,        
            "4_STORY_SHIRO_27": self._4_story_shiro_27,        
            "4_STORY_SHIRO_28": self._4_story_shiro_28,        
            "4_STORY_SHIRO_29": self._4_story_shiro_29,        
            "4_STORY_SHIRO_30": self._4_story_shiro_30,        
            "4_STORY_SHIRO_31": self._4_story_shiro_31,        
            "4_STORY_SHIRO_32": self._4_story_shiro_32,        
            "4_STORY_SHIRO_33": self._4_story_shiro_33,        
            "4_STORY_SHIRO_34": self._4_story_shiro_34,        
            "4_STORY_SHIRO_35": self._4_story_shiro_35,        
            "4_STORY_SHIRO_36": self._4_story_shiro_36,        
            "4_STORY_SHIRO_37": self._4_story_shiro_37,        
            "4_STORY_SHIRO_38": self._4_story_shiro_38,        
            "4_STORY_SHIRO_39": self._4_story_shiro_39,        
            "4_STORY_SHIRO_40": self._4_story_shiro_40,        
            "4_STORY_SHIRO_41": self._4_story_shiro_41,        
            "4_STORY_SHIRO_42": self._4_story_shiro_42,        
            "4_STORY_SHIRO_43": self._4_story_shiro_43,        
            "4_STORY_SHIRO_44": self._4_story_shiro_44,        
            "4_STORY_SHIRO_45": self._4_story_shiro_45,        
            "4_STORY_SHIRO_46": self._4_story_shiro_46,        
            "4_STORY_SHIRO_47": self._4_story_shiro_47,        
            "4_STORY_SHIRO_48": self._4_story_shiro_48,        
            "4_STORY_SHIRO_49": self._4_story_shiro_49,        
            "4_STORY_SHIRO_50": self._4_story_shiro_50,        
            "4_STORY_SHIRO_51": self._4_story_shiro_51,        
            "4_STORY_SHIRO_52": self._4_story_shiro_52,        
            "4_STORY_SHIRO_53": self._4_story_shiro_53,        
            "4_STORY_SHIRO_54": self._4_story_shiro_54,        
            "4_STORY_SHIRO_55": self._4_story_shiro_55,        
            "4_STORY_SHIRO_56": self._4_story_shiro_56,        
            "4_STORY_SHIRO_57": self._4_story_shiro_57,        
            "4_STORY_SHIRO_58": self._4_story_shiro_58,        
            "4_STORY_SHIRO_59": self._4_story_shiro_59,        
            "4_STORY_SHIRO_60": self._4_story_shiro_60,        
            "4_STORY_SHIRO_61": self._4_story_shiro_61,        
            "4_STORY_SHIRO_62": self._4_story_shiro_62,        
            "4_STORY_SHIRO_63": self._4_story_shiro_63,        
            "4_STORY_SHIRO_64": self._4_story_shiro_64,        
            "4_STORY_SHIRO_65": self._4_story_shiro_65,        
            "4_STORY_SHIRO_66": self._4_story_shiro_66,        
            "4_STORY_SHIRO_67": self._4_story_shiro_67,        
            "4_STORY_SHIRO_68": self._4_story_shiro_68,        
            "4_STORY_SHIRO_69": self._4_story_shiro_69,        
            "4_STORY_SHIRO_70": self._4_story_shiro_70,       
            "4_STORY_SHIRO_71": self._4_story_shiro_71,       
            "4_STORY_SHIRO_72": self._4_story_shiro_72,       
            "4_STORY_SHIRO_73": self._4_story_shiro_73,       
            "4_STORY_SHIRO_74": self._4_story_shiro_74,       
            "4_STORY_SHIRO_75": self._4_story_shiro_75,       
            "4_STORY_SHIRO_76": self._4_story_shiro_76,       
            "4_STORY_SHIRO_77": self._4_story_shiro_77,       
            "4_STORY_SHIRO_78": self._4_story_shiro_78,       
            "4_STORY_SHIRO_79": self._4_story_shiro_79,       
            "4_STORY_SHIRO_80": self._4_story_shiro_80,       
            "4_STORY_SHIRO_81": self._4_story_shiro_81,       
            "4_STORY_SHIRO_82": self._4_story_shiro_82,       
            "4_STORY_SHIRO_83": self._4_story_shiro_83,       
            "4_STORY_SHIRO_84": self._4_story_shiro_84,       
            "4_STORY_SHIRO_85": self._4_story_shiro_85,       
            "4_STORY_SHIRO_86": self._4_story_shiro_86,       
            "4_STORY_SHIRO_87": self._4_story_shiro_87,       
            "4_STORY_SHIRO_88": self._4_story_shiro_88, 
                  

            "4_STORY_END": self._4_story_end,
        }
        self._4_story_current_state="4_STORY_START_CHECK" 
        self._4_story_current_state_init= "4_STORY_SHIRO_84"
        
        self.STATE_5_STORY_FUNCTION = {
            "5_STORY_START_CHECK": self._5_story_start_check,
            "5_STORY_MAPPING_1": self._5_story_mapping_1,
            "5_STORY_MAPPING_2": self._5_story_mapping_2,
            "5_STORY_MAPPING_3": self._5_story_mapping_3,
            "5_STORY_MAPPING_4": self._5_story_mapping_4,
            "5_STORY_MAPPING_5": self._5_story_mapping_5,
            "5_STORY_MAPPING_6": self._5_story_mapping_6,            
            
            "5_STORY_D_LANK_BATTLE_ZONE": self._5_story_d_lank_battle_zone,
            
            "5_STORY_KARASUBA_1": self._5_story_karasuba_1, 
            "5_STORY_KARASUBA_2": self._5_story_karasuba_2, 
            "5_STORY_KARASUBA_3": self._5_story_karasuba_3, 
            "5_STORY_KARASUBA_4": self._5_story_karasuba_4, 
            "5_STORY_KARASUBA_5": self._5_story_karasuba_5, 
            "5_STORY_KARASUBA_6": self._5_story_karasuba_6, 
            "5_STORY_KARASUBA_7": self._5_story_karasuba_7, 
            "5_STORY_KARASUBA_8": self._5_story_karasuba_8, 
            "5_STORY_KARASUBA_9": self._5_story_karasuba_9, 
            "5_STORY_KARASUBA_10": self._5_story_karasuba_10, 
            "5_STORY_KARASUBA_11": self._5_story_karasuba_11, 
            "5_STORY_KARASUBA_12": self._5_story_karasuba_12, 
            "5_STORY_KARASUBA_13": self._5_story_karasuba_13, 
            "5_STORY_KARASUBA_14": self._5_story_karasuba_14, 
            "5_STORY_KARASUBA_15": self._5_story_karasuba_15, 
            "5_STORY_KARASUBA_16": self._5_story_karasuba_16, 
            "5_STORY_KARASUBA_17": self._5_story_karasuba_17, 
            "5_STORY_KARASUBA_18": self._5_story_karasuba_18, 
            "5_STORY_KARASUBA_19": self._5_story_karasuba_19, 
            "5_STORY_KARASUBA_20": self._5_story_karasuba_20, 
            "5_STORY_KARASUBA_21": self._5_story_karasuba_21, 
            "5_STORY_KARASUBA_22": self._5_story_karasuba_22, 
            "5_STORY_KARASUBA_23": self._5_story_karasuba_23, 
            "5_STORY_KARASUBA_24": self._5_story_karasuba_24, 
            "5_STORY_KARASUBA_25": self._5_story_karasuba_25, 
            "5_STORY_KARASUBA_26": self._5_story_karasuba_26, 
            "5_STORY_KARASUBA_27": self._5_story_karasuba_27, 
            "5_STORY_KARASUBA_28": self._5_story_karasuba_28, 
            "5_STORY_KARASUBA_29": self._5_story_karasuba_29, 
            "5_STORY_KARASUBA_30": self._5_story_karasuba_30, 
            "5_STORY_KARASUBA_31": self._5_story_karasuba_31, 
            "5_STORY_KARASUBA_32": self._5_story_karasuba_32, 
            "5_STORY_KARASUBA_33": self._5_story_karasuba_33, 
            "5_STORY_KARASUBA_34": self._5_story_karasuba_34, 
            "5_STORY_KARASUBA_35": self._5_story_karasuba_35, 
            "5_STORY_KARASUBA_36": self._5_story_karasuba_36, 
            "5_STORY_KARASUBA_37": self._5_story_karasuba_37, 
            "5_STORY_KARASUBA_38": self._5_story_karasuba_38, 
            "5_STORY_KARASUBA_39": self._5_story_karasuba_39, 
            "5_STORY_KARASUBA_40": self._5_story_karasuba_40, 
            "5_STORY_KARASUBA_41": self._5_story_karasuba_41, 
            "5_STORY_KARASUBA_42": self._5_story_karasuba_42, 
            "5_STORY_KARASUBA_43": self._5_story_karasuba_43,  
            "5_STORY_KARASUBA_44": self._5_story_karasuba_44,  
            "5_STORY_KARASUBA_45": self._5_story_karasuba_45,  
            "5_STORY_KARASUBA_46": self._5_story_karasuba_46,  
            "5_STORY_KARASUBA_47": self._5_story_karasuba_47,  
            "5_STORY_KARASUBA_48": self._5_story_karasuba_48,  
            "5_STORY_KARASUBA_49": self._5_story_karasuba_49,  
            "5_STORY_KARASUBA_50": self._5_story_karasuba_50,  
            "5_STORY_KARASUBA_51": self._5_story_karasuba_51,   
            "5_STORY_KARASUBA_52": self._5_story_karasuba_52,   
            "5_STORY_KARASUBA_53": self._5_story_karasuba_53,   
            "5_STORY_KARASUBA_54": self._5_story_karasuba_54,   
            "5_STORY_KARASUBA_55": self._5_story_karasuba_55,   
            "5_STORY_KARASUBA_56": self._5_story_karasuba_56,   
            "5_STORY_KARASUBA_57": self._5_story_karasuba_57,   
            "5_STORY_KARASUBA_58": self._5_story_karasuba_58,   
            "5_STORY_KARASUBA_59": self._5_story_karasuba_59,   
            "5_STORY_KARASUBA_60": self._5_story_karasuba_60,   
            "5_STORY_KARASUBA_61": self._5_story_karasuba_61,   
            "5_STORY_KARASUBA_62": self._5_story_karasuba_62,   
            "5_STORY_KARASUBA_63": self._5_story_karasuba_63,   
            "5_STORY_KARASUBA_64": self._5_story_karasuba_64,   
            "5_STORY_KARASUBA_65": self._5_story_karasuba_65,   
            "5_STORY_KARASUBA_66": self._5_story_karasuba_66,   
            "5_STORY_KARASUBA_67": self._5_story_karasuba_67,   
            "5_STORY_KARASUBA_68": self._5_story_karasuba_68,   
            "5_STORY_KARASUBA_69": self._5_story_karasuba_69,   
            "5_STORY_KARASUBA_70": self._5_story_karasuba_70,   
            "5_STORY_KARASUBA_71": self._5_story_karasuba_71,   
            "5_STORY_KARASUBA_72": self._5_story_karasuba_72,   
            "5_STORY_KARASUBA_73": self._5_story_karasuba_73,   
            "5_STORY_KARASUBA_74": self._5_story_karasuba_74,   
            "5_STORY_KARASUBA_75": self._5_story_karasuba_75,   
            "5_STORY_KARASUBA_76": self._5_story_karasuba_76,   
            "5_STORY_KARASUBA_77": self._5_story_karasuba_77,   
            "5_STORY_KARASUBA_78": self._5_story_karasuba_78,   
            "5_STORY_KARASUBA_79": self._5_story_karasuba_79,   
            "5_STORY_KARASUBA_80": self._5_story_karasuba_80,   
            "5_STORY_KARASUBA_81": self._5_story_karasuba_81,   
            "5_STORY_KARASUBA_82": self._5_story_karasuba_82,    
            "5_STORY_KARASUBA_83": self._5_story_karasuba_83,    
            "5_STORY_KARASUBA_84": self._5_story_karasuba_84,    
            "5_STORY_KARASUBA_85": self._5_story_karasuba_85,    
            "5_STORY_KARASUBA_86": self._5_story_karasuba_86,    
            "5_STORY_KARASUBA_87": self._5_story_karasuba_87,    
            "5_STORY_KARASUBA_88": self._5_story_karasuba_88,    
            "5_STORY_KARASUBA_89": self._5_story_karasuba_89,    
            "5_STORY_KARASUBA_90": self._5_story_karasuba_90,    
            "5_STORY_KARASUBA_91": self._5_story_karasuba_91,    
            "5_STORY_KARASUBA_92": self._5_story_karasuba_92,    
            "5_STORY_KARASUBA_93": self._5_story_karasuba_93,    
            "5_STORY_KARASUBA_94": self._5_story_karasuba_94,    
            "5_STORY_KARASUBA_95": self._5_story_karasuba_95,    
            "5_STORY_KARASUBA_96": self._5_story_karasuba_96,    
            "5_STORY_KARASUBA_97": self._5_story_karasuba_97,    
            "5_STORY_KARASUBA_98": self._5_story_karasuba_98,    
            "5_STORY_KARASUBA_99": self._5_story_karasuba_99,    
            "5_STORY_KARASUBA_100": self._5_story_karasuba_100,    
            "5_STORY_KARASUBA_101": self._5_story_karasuba_101,    
            "5_STORY_KARASUBA_102": self._5_story_karasuba_102,     
            "5_STORY_KARASUBA_103": self._5_story_karasuba_103,     
            "5_STORY_KARASUBA_104": self._5_story_karasuba_104,     
            "5_STORY_KARASUBA_105": self._5_story_karasuba_105,     
            "5_STORY_KARASUBA_106": self._5_story_karasuba_106,     
            "5_STORY_KARASUBA_107": self._5_story_karasuba_107,     
            "5_STORY_KARASUBA_108": self._5_story_karasuba_108,     
            "5_STORY_KARASUBA_109": self._5_story_karasuba_109,     
            "5_STORY_KARASUBA_110": self._5_story_karasuba_110,     
            "5_STORY_KARASUBA_111": self._5_story_karasuba_111,     
            "5_STORY_KARASUBA_112": self._5_story_karasuba_112,     
            "5_STORY_KARASUBA_113": self._5_story_karasuba_113,     
            "5_STORY_KARASUBA_114": self._5_story_karasuba_114,     
            "5_STORY_KARASUBA_115": self._5_story_karasuba_115,     
            "5_STORY_KARASUBA_116": self._5_story_karasuba_116,     
            "5_STORY_KARASUBA_117": self._5_story_karasuba_117,     
            "5_STORY_KARASUBA_118": self._5_story_karasuba_118,     
            "5_STORY_KARASUBA_119": self._5_story_karasuba_119,     
            "5_STORY_KARASUBA_120": self._5_story_karasuba_120,     
            "5_STORY_KARASUBA_121": self._5_story_karasuba_121,      
            "5_STORY_KARASUBA_122": self._5_story_karasuba_122,      
            "5_STORY_KARASUBA_123": self._5_story_karasuba_123,      
            "5_STORY_KARASUBA_124": self._5_story_karasuba_124,      
        
            "5_STORY_END": self._5_story_end,
        }
        self._5_story_current_state="5_STORY_START_CHECK" 
        self._5_story_current_state_init= "5_STORY_KARASUBA_123"

        self.STATE_6_STORY_FUNCTION = {
            "6_STORY_START_CHECK": self._6_story_start_check,
            
            "6_STORY_MAPPING_1": self._6_story_mapping_1,
            "6_STORY_MAPPING_2": self._6_story_mapping_2,
            "6_STORY_MAPPING_3": self._6_story_mapping_3,
            "6_STORY_MAPPING_4": self._6_story_mapping_4,            
            
            "6_STORY_C_LANK_BATTLE_ZONE": self._6_story_c_lank_battle_zone,
            
            #"6_STORY_YUKARI_1"
            
            
            "6_STORY_END": self._6_story_end,
        }
        self._6_story_current_state="6_STORY_START_CHECK" 
        self._6_story_current_state_init= "6_STORY_START_CHECK" 
        
        self.STATE_7_STORY_FUNCTION = {
            "7_STORY_START_CHECK": self._7_story_start_check,
            
            
            "7_STORY_END": self._7_story_end,
        }
        self._7_story_current_state="7_STORY_START_CHECK" 
        self._7_story_current_state_init= "7_STORY_START_CHECK" 
        
        self.STATE_8_STORY_FUNCTION = {
            "8_STORY_START_CHECK": self._8_story_start_check,
            
            
            "8_STORY_END": self._8_story_end,
        }
        self._8_story_current_state="8_STORY_START_CHECK" 
        self._8_story_current_state_init= "8_STORY_START_CHECK" 
        
        
    ######################################################
    # Commonfunction
    ######################################################
        self.STATE_COMMON_BOX_CHANGE_FUNCTION = {
            "COMMON_BOX_CHANGE_START": self.common_skill_change_start,
            "COMMON_BOX_CHANGE_START_CHECK": self.common_skill_change_start_check,
            "COMMON_BOX_CHANGE_BOX_OPEN": self.common_box_change_box_open,
            "COMMON_BOX_CHANGE_BOX_TARGET1": self.common_box_change_box_target1,
            "COMMON_BOX_CHANGE_BOX_TARGET1_SELECT": self.common_box_change_box_target1_select,
            "COMMON_BOX_CHANGE_BOX_TARGET2": self.common_box_change_box_target2,
            "COMMON_SKILL_CHANGE_SKILL_WINDOW_CLOSE": self.common_box_change_window_close,
            "COMMON_SKILL_CHANGE_END": self.common_skill_change_end,
            }
        self.common_box_change_current_state="COMMON_BOX_CHANGE_START"

        self.STATE_COMMON_SKILL_CHANGE_FUNCTION = {
            "COMMON_SKILL_CHANGE_START": self.common_skill_change_start,
            "COMMON_SKILL_CHANGE_START_CHECK": self.common_skill_change_start_check,
            "COMMON_SKILL_CHANGE_POKEMON_SELECT": self.common_skill_change_pokemon_select,
            "COMMON_SKILL_CHANGE_SKILL_WINDOW_OPEN": self.common_skill_change_skill_window_open,
            "COMMON_SKILL_CHANGE_SKILL_WINDOW_CHTARGET1": self.common_skill_change_skill_window_chtarget1,
            "COMMON_SKILL_CHANGE_SKILL_WINDOW_CHTARGET2": self.common_skill_change_skill_window_chtarget2,
            "COMMON_SKILL_CHANGE_SKILL_WINDOW_CLOSE": self.common_skill_change_skill_window_close,
            "COMMON_SKILL_CHANGE_END": self.common_skill_change_end,
            "COMMON_SKILL_CHANGE_FALSE": self.common_skill_change_false,
            }
        self.common_skill_change_current_state="COMMON_SKILL_CHANGE_START"

        self.STATE_COMMON_ITEM_GIVE_FUNCTION = {
            "COMMON_ITEM_GIVE_START": self.common_skill_change_start,
            "COMMON_ITEM_GIVE_START_CHECK": self.common_skill_change_start_check,
            "COMMON_ITEM_GIVE_POKEMON_SELECT": self.common_skill_change_pokemon_select,
            "COMMON_ITEM_GIVE_WINDOW_OPEN": self.common_item_give_window_open,
            "COMMON_ITEM_GIVE_TARGET_SIDE": self.common_item_give_target_side,
            "COMMON_ITEM_GIVE_TARGET_HIGH": self.common_item_give_target_high,
            "COMMON_ITEM_GIVE_WINDOW_CLOSE": self.common_item_give_window_close,
            "COMMON_ITEM_GIVE_END": self.common_item_give_end,
            }
        self.common_item_give_current_state="COMMON_ITEM_GIVE_START"


        self.STATE_COMMON_FUNCTION = {
            "COMMON_START": self.Common_start,
            "COMMON_MAP_OPEN": self.Common_map_open,
            "COMMON_GOTO_SELECT1": self.Common_goto_select1,
            "COMMON_GOTO_SELECT2": self.Common_goto_select2,
            "COMMON_CHANGE_TIME": self.Common_change_time,
            "COMMON_CHECK_TIME": self.Common_check_time,
            "COMMON_GOTO_JUMP" : self.Common_goto_jump#dummy
            
            #"COMMON_BATTLE_RETURN" : self.Common_battle_return,
        }
        self.Common_current_state="COMMON_START"
        self.map_cursor_reset=0
        
    ######################################################
    # Commonfunction
    ######################################################
    
    ######################################################
    # ZA_battle_infi_Base
    ######################################################
        self.sleepcount=0
        self.battlecount=0
        self.battle_step=0
        self.battle_step_return=0
        self.show_value_bool = False
        self.show_value_bool2 = self.show_value_bool
        self.chicketmaxflag = 0
        #self.ZL_state = 0
        self.Rstick_state = 0
        self.Lstick_state = 0
        self.Lstick_state2 = 0
        self.Lstick_state3 = 0
        self.Lstick_state4 = 0
        self.Lstick_state_m1 = 0
        self.Lstick_state_m2 = 0
        
        self.quasarcount = 0
        self.quasarlosecount = 0
        self.targetzone = 1
        self.timecount=0
        
        self.testcode=0
        self.testtarget=6
        
        self.fastread=True
        self.battleescapecount=0
        self.changetimecount=0
        self.changetimemisscount=0
        
        self.inactioncount=0
        self.battlecheck=0
        self.notarget_movecount=0
        
        self.SEE_DEFAULT=0.6
        self.SEE_LOW=0.3
        self.see_r=self.SEE_DEFAULT
        self.quasar_battle_lockon=0
        self.notargetcount=0
        self.escapecheckrange = 50
        # ポケモン選択間隔 ,マップ選択間隔 ,ZL間隔 ,バトルゾーン判断開始までの猶予期間 ,RIGHT_Stick間隔
        #self.sleetimes = [0.25,0.2,0.01,0.4,0,13]
        
        self.config_path="Commands/PythonCommands/ZA_story/zones.jsonc"
        self.config_path2="Commands/PythonCommands/ZA_story/sleeps.jsonc"
        
        self.STATE_ZA_INFI_MAIN_FUNCTION = {
            "ZA_INFI_MAIN_START": self.za_infi_main_start,
            "ZA_INFI_MAIN_BENCH": self.za_infi_main_bench,
            "ZA_INFI_MAIN_BATTLE_LOOP": self.za_infi_main_battle_loop,
            "ZA_INFI_MAIN_END": self.za_infi_main_end,
            "ZA_INFI_QUASAR_LOOP": self.za_infi_quasar_loop,
        }
        self.za_infi_main_current_state="ZA_INFI_MAIN_START"
        
        self.STATE_BENCH_FUNCTION = {
            "BENCH_START": self.bench_start,
            "BENCH_MAP_OPEN": self.bench_map_open,
            "BENCH_POKECENTER_SELECT1": self.bench_goto_pokecenter1,
            "BENCH_POKECENTER_SELECT2": self.bench_goto_pokecenter2,
            "BENCH_CHANGE_TIME": self.bench_change_time,
            "BENCH_CHECK_TIME": self.bench_check_time,
            "BENCH_CHANGE_TIME2": self.bench_change_time,
            
            "QUASAR_MAP_OPEN" : self.quasar_map_open,
            "QUASAR_SELECT1": self.goto_quasar1,
            "QUASAR_SELECT2": self.goto_quasar2,
            
            "BATTLE_RETURN": self.battle_return
        }
        self.bench_current_state="BENCH_START"
        
        self.STATE_BATTLE_FUNCTION = {
            "BATTLE_START": self.battle_start,
            "BATTLE_MAP_OPEN": self.battle_map_open,
            "BATTLE_GOTO_BATTLE_ZONE1": self.battle_goto_battle_zone1,
            "BATTLE_GOTO_BATTLE_ZONE2": self.battle_goto_battle_zone2,
            "BATTLE_MOVE": self.battle_move
        }
        self.battle_current_state="BATTLE_START"

        self.STATE_QUASAR_FUNCTION = {
            "QUASAR_START": self.quasar_start,
            "QUASAR_MOVE_DOOR": self.quasar_move_door,
            "QUASAR_MOVE_ENTRANCE": self.quasar_move_entrance,
            "QUASAR_BATTLE_LOOP": self.quasar_battle_loop,
        }
        self.quasar_current_state="QUASAR_START"
                
        self.ZONELIST = {}
        
        self.zonecount = [0,0,0,0,0,0,0,0,0,0,0,0]
        self.zonemisscount = [0,0,0,0,0,0,0,0,0,0,0,0]
        self.targetzone = 1
        
        self.SLEEPLIST = {}
        
        # 50以下,55以下,60以下,65以下,70以下,75以下,80以下,85以下,90以下,95以下,100以下
        self.target_left_max_val_list = [0,0,0,0,0,0,0,0,0,0,0]
        self.target_right_max_val_list = [0,0,0,0,0,0,0,0,0,0,0]
        
        #PythonCoomandBase.pyの追加コードを使用(基本0としてください)
        #self.TESTADDCODE=1
        
        self.target_start_low_count=0
        self.target_end_low_count=0
        self.target_start_count=0
        self.target_end_count=0
        self.target_start_mid_count=0
        self.target_end_mid_count=0
        
        self.quasar_target_start_low_count=0
        self.quasar_target_end_low_count=0
        self.quasar_target_start_count=0
        self.quasar_target_end_count=0
        self.quasar_target_start_mid_count=0
        self.quasar_target_end_mid_count=0  
        
        self.quasar_battle_display_start_count=0
        self.quasar_battle_display_end_count=0
      
        self.battle_nofiled_count=0
        self.battle_nofiled_count_max =30
        self.battlemarker_skipcount_threshold=3
        self.battlemarker_skipcount=self.battlemarker_skipcount_threshold
        
        self.battle_zone_loop_num = 3
        self.no_Cplus=1
    ######################################################
    # ZA_battle_infi_Base_End
    ######################################################
    
    def load_json_with_comments(self, filename):
        """コメント付きJSONを読み込む関数（// や # 行を無視）"""
        with open(filename, "r", encoding="utf-8") as f:
            lines = []
            for line in f:
                stripped = line.strip()
                # コメントや空行をスキップ
                if stripped.startswith("//") or stripped.startswith("#") or stripped == "":
                    continue
                lines.append(line)
            json_text = "".join(lines)
            return json.loads(json_text)

    def save_sleeps(self):
        """SLEEPLISTをJSONファイルに保存（整形付き）"""
        try:
            # キーを文字列に変換して保存（JSONでは数値キーが文字列化されるため）
            data_to_save = {str(k): v for k, v in self.SLEEPLIST.items()}
            
            with open(self.config_path2, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)
            
            print("SLEEPLISTをファイルに保存しました。")
        except Exception as e:
            print(f"SLEEPLISTの保存エラー: {e}")

    def load_zones(self):
        added, changed = [], []
        """ファイルからZONELISTを更新"""
        try:
            data = self.load_json_with_comments(self.config_path)
            # JSONではキーが文字列になるのでintキーに変換
            self.ZONELIST = {int(k): v for k, v in data.items()}
            print("ZONELISTを更新しました。")
            if not added and not changed:
                print("（変更はありません）")
            elif self.ZONELIST[key] != value:
                print(f"ZONE {key} が更新されました。")
                print(f"旧: {self.ZONELIST[key]}")
                print(f"新: {value}")
                changed.append(key)
        except Exception as e:
            print(f"ZONELISTの読み込みエラー: {e}")
            
    def load_sleeps(self):
        added, changed = [], []  
        try:
            data = self.load_json_with_comments(self.config_path2)
            # JSONではキーが文字列になるのでintキーに変換
            self.SLEEPLIST = {int(k): v for k, v in data.items()}
            print("SLEEPLISTを更新しました。")
            if not added and not changed:
                print("（変更はありません）")
            elif self.SLEEPLIST[key] != value:
                print(f"SLEEP {key} が更新されました。")
                print(f"旧: {self.SLEEPLIST[key]}")
                print(f"新: {value}")
                changed2.append(key)
        except Exception as e:
            print(f"SLEEPLISTの読み込みエラー: {e}")

    def watch_file(self):
        """ファイル変更を監視して自動更新"""
        last_mtime = 0
        last_mtime2 = 0
        while True:
            try:
                mtime = os.path.getmtime(self.config_path)
                if mtime != last_mtime:
                    last_mtime = mtime
                    self.load_zones()
            except FileNotFoundError:
                print("zones.jsonc が見つかりません。")
                
        while True:
            try:
                mtime2 = os.path.getmtime(self.config_path2)
                if mtime2 != last_mtime2:
                    last_mtime2 = mtime2
                    self.load_sleeps()
            except FileNotFoundError:
                print("sleeps.jsonc が見つかりません。")
        
    ######################################################
    # Command
    ######################################################
    def sendCommand(self, row: str, wait: float = 0.04):
        self.keys.ser.ser.write((row + '\r\n').encode('utf-8'))
        self.wait(wait)
        self.checkIfAlive()

    def etc_sendCommand(self,str, wait: float = 0.04):
        Lbutton_down1  = "0x0000 4"
        Lbutton_down2  = "0x0000 8"
        Bbutton1  = "0x0008 8"
        Bbutton2  = "0x0000 8"
        Lbutton_up1  = "0x0000 0"
        Lbutton_up2  = "0x0000 8"
        Lbutton_left1  = "0x0000 6"
        Lbutton_left2  = "0x0000 8"
        Lbutton_right1  = "0x0000 2"
        Lbutton_right2  = "0x0000 8"
        plusbutton1  = "0x0800 8"
        plusbutton2  = "0x0000 8"
        Lbutton_rab1  = "0x0018 6"
        Lbutton_rb1  = "0x0008 6"

        if str == "Lbutton_down":
            self.sendCommand(Lbutton_down1,wait)
            self.sendCommand(Lbutton_down2,wait)
        elif str == "Lbutton_up":
            self.sendCommand(Lbutton_up1,wait)
            self.sendCommand(Lbutton_up2,wait)
        elif str == "Lbutton_up_push":
            self.sendCommand(Lbutton_up1,wait)
        elif str == "Lbutton_up_pull":
            self.sendCommand(Lbutton_up2,wait)
            
        elif str == "Lbutton_left":
            self.sendCommand(Lbutton_left1,wait)
            self.sendCommand(Lbutton_left2,wait)              
        elif str == "Lbutton_right":
            self.sendCommand(Lbutton_right1,wait)
            self.sendCommand(Lbutton_right2,wait)
        elif str == "plusbutton":
            self.sendCommand(plusbutton1,wait)
            self.sendCommand(plusbutton2,wait)
        elif str == "plusbutton_push":
            self.sendCommand(plusbutton1,wait)
        elif str == "plusbutton_release":
            self.sendCommand(plusbutton2,wait)

    # ウインドウ取得関数 (win32gui仕様)
    def window_acquire(Window_name:str,log=False,front_win=False):
        hwnd_dict = {}
        result = None
        if front_win:
            hwnd = win32gui.GetForegroundWindow() # 最前面ウィンドウのウィンドウハンドルを取得
        
        else:
            key = value = []
            def winEnumHandler(hwnd,ctx):
                if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
                    key.append(hex(hwnd))
                    value.append(win32gui.GetWindowText(hwnd))
                hwnd_dict.update(zip(key, value))

            win32gui.EnumWindows(winEnumHandler, None)
            hwnd_dict.update(zip(key,value))

            # 部分一致で検索
            for wd_class in hwnd_dict.keys():
                # 最初にヒットしたウインドウを取得
                if Window_name in hwnd_dict[wd_class]:
                    result = hwnd_dict[wd_class]
                    if log: print(wd_class,result)
                    break
            else:
                return None

            if log:
                print('--------ウインドウ一覧--------')
                print(json.dumps(hwnd_dict, sort_keys=False, indent=2, ensure_ascii=False))  # なんかいい感じに表示

            # ウィンドウタイトルでウィンドウハンドルを取得  第一引数はクラス名、なければNone  第二引数はタイトル名(完全一致)
            hwnd = win32gui.FindWindow(None,result)

        # 座標取得
        rect = win32gui.GetWindowRect(hwnd)

        x, y = rect[0], rect[1]
        w, h = rect[2] - x, rect[3] - y
        x_center, y_center = x + w/2 , y + h/2
        #      0  1  2  3        4              5          6       7        8   
        ret = [x, y, w, h, int(x_center), int(y_center), hwnd, hwnd_dict, result]
        
        if log:
            print(f'window info: {ret}')
            print(  f" Target_Window:{result}\n"
                    f" Location:{x} {y}\n"
                    f" Size:{w} {h}\n"
                    f" Center:{x_center,y_center}" )

        return ret
    
    ######################################################
    # ZA_battle_infi_Base
    ######################################################
    def Benchi(self):
        if self.sleepcount==0:
            self.press(Direction(Stick.LEFT, 180), duration=0.7, wait=0.1)
            self.press(Direction(Stick.LEFT, 90), duration=0.5, wait=0.1)
        else:
            self.press(Direction(Stick.LEFT, 270), duration=0.5, wait=0.1)
        self.pressRep(Button.A, repeat=12, duration=0.15, wait=0.2, interval=0.3)

    def zone_check(self):
        self.wait(self.SLEEPLIST[3][2])
        for i in range(1,13):
            if self.image_check(self.ZONELIST[i][0],1):
                self.zonecount[i-1] += 1
                return i
        return 12
    
    def MOVE_ACTION(self,movestep,lockonflg=1):
        start = time.perf_counter()  # 計測開始
        count= 0
        waitflg=0
        waitstart = time.perf_counter() 
        if self.image_check("EYE_CHECK_HIGH"):
            return movestep
        elif self.ZONELIST[self.targetzone][5 + movestep][3] and self.image_check("EYE_CHECK"):
            return movestep
        if self.ZONELIST[self.targetzone][5 + movestep][0]:
            
            self.hold(Direction(Stick.LEFT, self.ZONELIST[self.targetzone][5 + movestep][1]))
            self.wait(self.SLEEPLIST[5][2])
            self.press(Button.B, wait=0.0)
            while True:

                if count % 30 == 0:
                    self.ZL_ACTION(lockonflg=lockonflg)
                if self.ZL_state == 1:
                    self.press(Button.A, wait=0.0)
                    if (self.no_Cplus==0 and self.image_check("C+")):
                        self.holdEnd(Direction(Stick.LEFT, self.ZONELIST[self.targetzone][5 + movestep][1]))
                        return movestep
                
                if self.image_check("ESCAPE"):
                    self.holdEnd(Direction(Stick.LEFT, self.ZONELIST[self.targetzone][5 + movestep][1]))
                    return movestep

                end = time.perf_counter()
                elapsed = end - start
                waitelapsed = end - waitstart
                if waitflg == 1 and waitelapsed > self.ZONELIST[self.targetzone][5 + movestep][4] :
                    self.holdEnd(Direction(Stick.LEFT, self.ZONELIST[self.targetzone][5 + movestep][1]))
                    
                    if (movestep + 1 ) < self.ZONELIST[self.targetzone][3]:
                        return (movestep + 1)
                    else:
                        return movestep
                elif elapsed > self.ZONELIST[self.targetzone][5 + movestep][2] \
                    or (self.image_check("ESCAPE") and self.battle_current_state == "BATTLE_MOVE"): 
                    self.holdEnd(Direction(Stick.LEFT, self.ZONELIST[self.targetzone][5 + movestep][1]))
                    
                    if (movestep + 1 ) < self.ZONELIST[self.targetzone][3]:
                        return (movestep + 1)
                    else:
                        return movestep
                elif self.image_check("EYE_CHECK_HIGH"):
                    self.holdEnd(Direction(Stick.LEFT, self.ZONELIST[self.targetzone][5 + movestep][1]))
                    
                    if (movestep + 1 ) < self.ZONELIST[self.targetzone][3]:
                        return (movestep + 1)
                    else:
                        return movestep
                elif self.ZONELIST[self.targetzone][5 + movestep][3] and self.image_check("EYE_CHECK"):
                    #ぎりぎりで止まると戦闘開始に行かないため遅延
                    waitstart = time.perf_counter() 
                    self.wait(self.ZONELIST[self.targetzone][5 + movestep][4])
                    waitflg=1
                    self.holdEnd(Direction(Stick.LEFT, self.ZONELIST[self.targetzone][5 + movestep][1]))
                    
                    if (movestep + 1 ) < self.ZONELIST[self.targetzone][3]:
                        return (movestep + 1)
                    else:
                        return movestep
                count +=1
        self.holdEnd(Direction(Stick.LEFT, self.ZONELIST[self.targetzone][5 + movestep][1]))          
        return movestep

    def MOVE_SEE2(self,action1 = "RELOAD",action2 = "RELOAD",in_see_r1=0.0,in_see_r2=0.0,dirnum=1,action = "RELOAD"):
        if action != "END":
            if self.Rstick_state == 0:
                self.hold(Direction(Stick.RIGHT, 180,local_see_r))
                self.Rstick_state = 1
            else:
                self.holdEnd(Direction(Stick.RIGHT, 180))
                self.wait(0.1)#self.wait(self.SLEEPLIST[4][2])
                self.hold(Direction(Stick.RIGHT, 180,local_see_r))
                self.Rstick_state = 1
        elif action == "END" and self.Rstick_state == 1:
            self.holdEnd(Direction(Stick.RIGHT, 180))
            self.Rstick_state = 0
    def MOVE_SEE(self,action = "RELOAD",in_see_r=0.0):
        if in_see_r==0.0:
            local_see_r = self.see_r
        else:
            local_see_r = in_see_r
            
        if (self.no_Cplus==1 and (not self.image_check("ESCAPE"))):#一旦視点移動はC+がない時のみ
            self.notargetcount=0
            if self.Rstick_state == 1:
                self.holdEnd(Direction(Stick.RIGHT, 180))
                self.Rstick_state = 0
            return
        if self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.quasar_battle_lockon==0:
            return
        if self.quasar_current_state=="QUASAR_BATTLE_LOOP":
            self.wait(0.1)
        if self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.no_Cplus==0 and self.image_check("C+"):
            self.notargetcount=0
            return
        if action != "END":
            if self.Rstick_state == 0:
                self.hold(Direction(Stick.RIGHT, 180,local_see_r))
                self.Rstick_state = 1
            else:
                self.holdEnd(Direction(Stick.RIGHT, 180))
                self.wait(0.1)#self.wait(self.SLEEPLIST[4][2])
                self.hold(Direction(Stick.RIGHT, 180,local_see_r))
                self.Rstick_state = 1
        elif action == "END" and self.Rstick_state == 1:
            self.holdEnd(Direction(Stick.RIGHT, 180))
            self.Rstick_state = 0
        #else:
        #    print(f"MOVE_SEE_CHECK:{action}:{self.Rstick_state}:")

    def MOVE_LStick(self,dir1,dir2,dir3,dir4,dirnum=1,action = "RELOAD"):
            
        if action != "END":
            if self.Lstick_state == 0 and self.Lstick_state2 == 0 and self.Lstick_state3 == 0 and self.Lstick_state4 == 0 and self.Lstick_state_m1 == 0 and self.Lstick_state_m2 == 0:
                if dirnum==1: 
                    self.hold(Direction(Stick.LEFT, dir1,1.0))
                    self.Lstick_state = 1
                elif dirnum==2: 
                    self.hold(Direction(Stick.LEFT, dir2,1.0))
                    self.Lstick_state2 = 1
                elif dirnum==3: 
                    self.hold(Direction(Stick.LEFT, dir3,1.0))
                    self.Lstick_state3 = 1
                elif dirnum==4: 
                    self.hold(Direction(Stick.LEFT, dir4,1.0))
                    self.Lstick_state4 = 1  
                #ロックオンマーカー時の視点変換用
                elif dirnum==-1: 
                    self.hold(Direction(Stick.LEFT, 50,0.1))
                    self.Lstick_state_m1 = 1
                elif dirnum==-2: 
                    self.hold(Direction(Stick.LEFT, 140,0.1))
                    self.Lstick_state_m2 = 1  
            else:
                if self.Lstick_state == 1:
                    self.holdEnd(Direction(Stick.LEFT, dir1))
                    self.Lstick_state = 0
                if self.Lstick_state2 == 1:
                    self.holdEnd(Direction(Stick.LEFT, dir2))
                    self.Lstick_state2 = 0
                if self.Lstick_state3 == 1:
                    self.holdEnd(Direction(Stick.LEFT, dir3))
                    self.Lstick_state3 = 0
                if self.Lstick_state4 == 1:
                    self.holdEnd(Direction(Stick.LEFT, dir4))
                    self.Lstick_state4 = 0
                #ロックオンマーカー時の視点変換用
                if self.Lstick_state_m1 == 1: 
                    self.holdEnd(Direction(Stick.LEFT, 50))
                    self.Lstick_state_m1 = 0
                if self.Lstick_state_m2 == 1: 
                    self.holdEnd(Direction(Stick.LEFT, 140))
                    self.Lstick_state_m2 = 0  
                    
                self.wait(0.1)#self.wait(self.SLEEPLIST[4][2])
                
                if dirnum==1: 
                    self.hold(Direction(Stick.LEFT, dir1,1.0))
                    self.Lstick_state = 1
                elif dirnum==2: 
                    self.hold(Direction(Stick.LEFT, dir2,1.0))
                    self.Lstick_state2 = 1
                elif dirnum==3: 
                    self.hold(Direction(Stick.LEFT, dir3,1.0))
                    self.Lstick_state3 = 1    
                elif dirnum==4: 
                    self.hold(Direction(Stick.LEFT, dir4,1.0))
                    self.Lstick_state4 = 1   
                #ロックオンマーカー時の視点変換用
                elif dirnum==-1: 
                    self.hold(Direction(Stick.LEFT, 50,0.1))
                    self.Lstick_state_m1 = 1 
                elif dirnum==-2: 
                    self.hold(Direction(Stick.LEFT, 140,0.1))
                    self.Lstick_state_m2 = 1 
        elif action == "END":
            if self.Lstick_state == 1:
                self.holdEnd(Direction(Stick.LEFT, dir1))
                self.Lstick_state = 0
            if self.Lstick_state2 == 1:
                self.holdEnd(Direction(Stick.LEFT, dir2))
                self.Lstick_state2 = 0
            if self.Lstick_state3 == 1:
                self.holdEnd(Direction(Stick.LEFT, dir3))
                self.Lstick_state3 = 0
            if self.Lstick_state4 == 1:
                self.holdEnd(Direction(Stick.LEFT, dir4))
                self.Lstick_state4 = 0
            #ロックオンマーカー時の視点変換用
            if self.Lstick_state_m1 == 1:
                self.holdEnd(Direction(Stick.LEFT, 50))
                self.Lstick_state_m1 = 0
            if self.Lstick_state_m2 == 1:
                self.holdEnd(Direction(Stick.LEFT, 140))
                self.Lstick_state_m2 = 0
                
    def ROTOM_GLIDE(self,dir,a_count,a_duration=0.15,a_wait=0.5,a_interval=0.1,move_r=1.0):
        self.hold(Direction(Stick.LEFT, dir,move_r))
        self.pressRep(Button.A, repeat=a_count, duration=a_duration, wait=a_wait, interval=a_interval)
        self.holdEnd(Direction(Stick.LEFT, dir))
    ######################################################
    # ZA_battle_infi_Base_End
    ######################################################
    def renda_button(self,rendabutton="B",endpicture="",endpicture2="",endpicture3="",endpicture4="",endpicture5="",endpicture6="",not_endpicture="FALSE_RETURN",sub_button="NULL",sub_picture="",sub2_button="NULL",sub2_picture="",sub3_button="NULL",sub3_picture="",sub4_button="NULL",sub4_picture="",sub5_button="NULL",sub5_picture="",sub6_button="NULL",sub6_picture="",sub7_button="NULL",sub7_picture="",event_picture="",sleeptime=0.5):
        while True:
            self.checkIfAlive()
            
            while True:
                checkerflg=0
                    
                #誤判定回避用で指定画面での検知を除外する
                if not self.image_check(not_endpicture):
                    if endpicture != "":
                        if self.image_check(endpicture):
                            return True
                    if endpicture2 != "":
                        if self.image_check(endpicture2):
                            return True
                    if endpicture3 != "":
                        if self.image_check(endpicture3):
                            return True
                    if endpicture4 != "":
                        if self.image_check(endpicture4):
                            return True     
                    if endpicture5 != "":
                        if self.image_check(endpicture5):
                            return True
                    if endpicture6 != "":
                        if self.image_check(endpicture6):
                            return True
                        
                if sub_picture != "":
                    if self.image_check(sub_picture):
                        if sub_button == "A":
                            self.pressRep(Button.A, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                            checkerflg=1
                            self.wait(sleeptime)
                if sub2_picture != "":
                    if self.image_check(sub2_picture):
                        if sub2_button == "A":
                            self.pressRep(Button.A, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                            checkerflg=1
                            self.wait(sleeptime)
                if sub3_picture != "":
                    if self.image_check(sub3_picture):
                        if sub3_button == "A":
                            self.pressRep(Button.A, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                            checkerflg=1
                            self.wait(sleeptime)
                if sub4_picture != "":
                    if self.image_check(sub4_picture):
                        if sub4_button == "A":
                            self.pressRep(Button.A, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                            checkerflg=1
                            self.wait(sleeptime)
                if sub5_picture != "":
                    if self.image_check(sub5_picture):
                        if sub5_button == "A":
                            self.pressRep(Button.A, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                            checkerflg=1
                            self.wait(sleeptime)
                if sub6_picture != "":
                    if self.image_check(sub6_picture):
                        if sub6_button == "A":
                            self.pressRep(Button.A, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                            checkerflg=1
                            self.wait(sleeptime)
                if sub7_picture != "":
                    if self.image_check(sub7_picture):
                        if sub7_button == "A":
                            self.pressRep(Button.A, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                            checkerflg=1
                            self.wait(sleeptime)
                            
                if event_picture != "":
                    if self.image_check(event_picture):
                        self.EventSkip_plus()
                        checkerflg=1
                        self.wait(sleeptime)
                     
                if checkerflg==0:
                    self.wait(sleeptime)
                    break

            if rendabutton == "B":
                self.pressRep(Button.B, repeat=1, duration=0.04, wait=0.0, interval=0.1)
            self.wait(sleeptime)
        return False
    
    def mega_evolution_battle_mode_select(self,mode=0,usenum=1):
        #アブソル Bはまもるのため選ばない。
        #if mode == 0 and self.mega_evolution_battle(Xaction=1,Aaction=1,Yaction=1,Baction=0,mode=0,dir1=320,dir2=20,see_r=0.20, endpicture="TEXT_WHITE_COMMENT"):
        if mode == 0 and self.mega_evolution_battle(usenum=usenum,Xaction=1,Aaction=1,Yaction=1,Baction=0,mode=0,dir1=20,dir2=340,dir3=60,dir4=300,see_r=0.24, endpicture="TEXT_WHITE_COMMENT"):

            return True
        
    def mega_evolution_battle(self,usenum=1,Xaction=0,Aaction=0,Yaction=0,Baction=0,mode=0,dir1=0,dir2=0,dir3=0,dir4=0,see_r=0, endpicture="",end2picture=""):
        count=0
        self.no_Cplus=0
        no_target_count=0
        no_target_count_threshold=0
        target_count=0
        target_count_threshold=0#10
        target_count_threshold2=3#10
        target_marker_count=0
        
        nofiled=1
        battle_count=0
        
        Cp_mode=0
        
        while True:
            if endpicture != "" or end2picture != "":
                if self.image_check(endpicture):
                    self.ZL_ACTION("END")
                    self.MOVE_LStick(dir1,dir2,dir3,dir4,1,"END")
                    self.MOVE_SEE(action = "END",in_see_r=see_r)
                    return True
                if self.image_check(end2picture):
                    self.ZL_ACTION("END")
                    self.MOVE_LStick(dir1,dir2,dir3,dir4,1,"END")
                    self.MOVE_SEE(action = "END",in_see_r=see_r)
                    return True
                
            if self.image_check("HELP_MARKER"):
                self.pressRep(Button.A, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                
            if self.image_check("R_push"):
                self.press(Button.RCLICK,0.05,0.1) 
                
            if nofiled==1 and (self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W")):
                if (usenum==1 and (self.image_check("FIELD1") or self.image_check("FIELD_BACK1"))):
                    self.wait(0.5)
                    self.etc_sendCommand("Lbutton_up")
                    nofiled=0
                elif (usenum==2 and (self.image_check("FIELD2") or self.image_check("FIELD_BACK2"))):
                    self.wait(0.5)
                    self.etc_sendCommand("Lbutton_up")
                    nofiled=0
                elif (usenum==3 and (self.image_check("FIELD3") or self.image_check("FIELD_BACK3"))):
                    self.wait(0.5)
                    self.etc_sendCommand("Lbutton_up")
                    nofiled=0
                elif (usenum==4 and (self.image_check("FIELD4") or self.image_check("FIELD_BACK4"))):
                    self.wait(0.5)
                    self.etc_sendCommand("Lbutton_up")
                    nofiled=0
                elif (usenum==5 and (self.image_check("FIELD5") or self.image_check("FIELD_BACK5"))):
                    self.wait(0.5)
                    self.etc_sendCommand("Lbutton_up")
                    nofiled=0
                elif (usenum==5 and (self.image_check("FIELD6") or self.image_check("FIELD_BACK6"))):
                    self.wait(0.5)
                    self.etc_sendCommand("Lbutton_up")
                    nofiled=0
                else:
                    self.etc_sendCommand("Lbutton_left")
                    self.wait(0.5)
                    continue
          
            self.ZL_ACTION("")
            if count==0 and Cp_mode==1:
                self.etc_sendCommand("plusbutton")
            for i in range(5):  
                if count==0 and Aaction==1 and self.image_check("C+"):
                    self.MOVE_SEE(action = "END")
                    self.pressRep(Button.A, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                    
                    #回避行動用
                    if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                        self.MOVE_LStick(dir1,dir2,dir3,dir4,4,"RELOAD")
                        if self.image_check("C+"):
                            self.ZL_ACTION("END")
                            self.pressRep(Button.Y, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                            self.ZL_ACTION("")
                            self.wait(0.3)
                            if not self.image_check("C+"):
                                self.MOVE_LStick(dir1,dir2,dir3,dir4,-1,"RELOAD")
                                self.pressRep(Button.L, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                                print("check0_0")
                            if not self.image_check("C+"):
                                self.wait(0.3)
                                self.MOVE_LStick(dir1,dir2,dir3,dir4,-2,"RELOAD")
                                self.pressRep(Button.L, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                                print("check0")
        
                        self.MOVE_SEE(action = "")
                        
                    self.ZL_ACTION("")
                    count=(count + 1) % 4
                    no_target_count=0
                    target_count+=1
                    continue
                    #QUICK_RETURN 回避動作間隔を狭めるため
                elif count==1 and Baction==1 and self.image_check("C+"):
                    self.MOVE_SEE(action = "END")
                    self.pressRep(Button.B, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                    #回避行動用
                    if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                        self.MOVE_LStick(dir1,dir2,dir3,dir4,4,"RELOAD")
                        if self.image_check("C+"):

                            self.ZL_ACTION("END")
                            self.pressRep(Button.Y, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                            self.ZL_ACTION("")
                            self.wait(0.3)
                            if not self.image_check("C+"):
                                self.MOVE_LStick(dir1,dir2,dir3,dir4,-1,"RELOAD")
                                self.pressRep(Button.L, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                                print("check1_0")
                            if not self.image_check("C+"):
                                self.wait(0.3)
                                self.MOVE_LStick(dir1,dir2,dir3,dir4,-2,"RELOAD")
                                self.pressRep(Button.L, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                                print("check1")
                        self.MOVE_SEE(action = "")

                    self.ZL_ACTION("")
                    count=(count + 1) % 4
                    no_target_count=0
                    target_count+=1
                    continue
                    #QUICK_RETURN 回避動作間隔を狭めるため
                elif count==2 and Xaction==1 and self.image_check("C+"):
                    self.MOVE_SEE(action = "END")
                    self.pressRep(Button.X, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                    #回避行動用
                    if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                        self.MOVE_LStick(dir1,dir2,dir3,dir4,4,"RELOAD")
                        if self.image_check("C+"):
                            self.ZL_ACTION("END")
                            self.pressRep(Button.Y, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                            self.ZL_ACTION("")
                            self.wait(0.3)
                            if not self.image_check("C+"):
                                self.MOVE_LStick(dir1,dir2,dir3,dir4,-1,"RELOAD")
                                self.pressRep(Button.L, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                                print("check2_0")
                            if not self.image_check("C+"):
                                self.wait(0.3)
                                self.MOVE_LStick(dir1,dir2,dir3,dir4,-2,"RELOAD")
                                self.pressRep(Button.L, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                                print("check2")
                        self.MOVE_SEE(action = "")

                    self.ZL_ACTION("")
                    count=(count + 1) % 4
                    no_target_count=0
                    target_count+=1
                    continue
                    #QUICK_RETURN 回避動作間隔を狭めるため
                elif count==3 and Yaction==1 and self.image_check("C+"):
                    self.MOVE_SEE(action = "END")
                    self.pressRep(Button.Y, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                    #回避行動用
                    if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                        self.MOVE_LStick(dir1,dir2,dir3,dir4,4,"RELOAD")
                        if self.image_check("C+"):
                            self.ZL_ACTION("END")
                            self.pressRep(Button.Y, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                            self.ZL_ACTION("")
                            self.wait(0.3)
                            if not self.image_check("C+"):
                                self.MOVE_LStick(dir1,dir2,dir3,dir4,-1,"RELOAD")
                                self.pressRep(Button.L, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                                print("check3_0")
                            if not self.image_check("C+"):
                                self.wait(0.3)
                                self.MOVE_LStick(dir1,dir2,dir3,dir4,-2,"RELOAD")
                                self.pressRep(Button.L, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                                print("check3")
                        self.MOVE_SEE(action = "")
                        
                    self.ZL_ACTION("")
                    count=(count + 1) % 4
                    no_target_count=0
                    target_count+=1
                    continue
                    #QUICK_RETURN 回避動作間隔を狭めるため
                elif not self.image_check("C+"):
                    self.ZL_ACTION("END")
                    self.wait(0.1)
                    self.ZL_ACTION("")

                    no_target_count+=1
                    target_count=0
                    break
                
            #回避行動中にターゲットマーカーチェックの移動を行えないと別方向に視点が行ってしまうため
            self.wait(1.0)   
            if not (self.image_check("TEXT_GREEN_COMMENT") or self.image_check("TEXT_BLACK_COMMENT")):    
                if (self.image_check("TARGET_LEFT_MID") or self.image_check("TARGET_RIGHT_MID") or self.image_check("TARGET_RIGHT_RIHGT_CHECK_MID") or self.image_check("TARGET_LEFT_RIHGT_CHECK_MID")):

                    if target_marker_count==2:
                        if not self.image_check("C+"):
                            self.MOVE_LStick(dir1,dir2,dir3,dir4,-1,"RELOAD")
                            self.pressRep(Button.L, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                        self.MOVE_SEE(action = "",in_see_r=see_r)
                        for i in range(5):
                            self.ZL_ACTION("END")
                            self.wait(0.1)
                            self.ZL_ACTION("")
                            if count==0 and Aaction==1 and self.image_check("C+"):
                                self.MOVE_SEE(action = "END")
                                self.pressRep(Button.A, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                                self.MOVE_SEE(action = "END",in_see_r=see_r)
                                self.wait(0.3)
                                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                                    if no_target_count>no_target_count_threshold:
                                        self.MOVE_LStick(dir1,dir2,dir3,dir4,3,"RELOAD")
                                    elif target_count>target_count_threshold2:
                                        self.MOVE_LStick(dir1,dir2,dir3,dir4,4,"RELOAD")
                                count=(count + 1) % 4
                                break
                            elif count==1 and Baction==1 and self.image_check("C+"):
                                self.MOVE_SEE(action = "END")
                                self.pressRep(Button.B, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                                self.MOVE_SEE(action = "END",in_see_r=see_r)
                                self.wait(0.3)
                                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                                    if no_target_count>no_target_count_threshold:
                                        self.MOVE_LStick(dir1,dir2,dir3,dir4,3,"RELOAD")
                                    elif target_count>target_count_threshold2:
                                        self.MOVE_LStick(dir1,dir2,dir3,dir4,4,"RELOAD")
                                count=(count + 1) % 4
                                break
                            elif count==2 and Xaction==1 and self.image_check("C+"):
                                self.MOVE_SEE(action = "END")
                                self.pressRep(Button.X, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                                self.MOVE_SEE(action = "END",in_see_r=see_r)
                                self.wait(0.3)
                                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                                    if no_target_count>no_target_count_threshold:
                                        self.MOVE_LStick(dir1,dir2,dir3,dir4,3,"RELOAD")
                                    elif target_count>target_count_threshold2:
                                        self.MOVE_LStick(dir1,dir2,dir3,dir4,4,"RELOAD")
                                count=(count + 1) % 4
                                break
                            elif count==3 and Yaction==1 and self.image_check("C+"):
                                self.MOVE_SEE(action = "END")
                                self.pressRep(Button.Y, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                                self.MOVE_SEE(action = "END",in_see_r=see_r)
                                self.wait(0.3)
                                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                                    if no_target_count>no_target_count_threshold:
                                        self.MOVE_LStick(dir1,dir2,dir3,dir4,3,"RELOAD")
                                    elif target_count>target_count_threshold2:
                                        self.MOVE_LStick(dir1,dir2,dir3,dir4,4,"RELOAD")
                                count=(count + 1) % 4
                                break
                            else:
                                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                                    if no_target_count>no_target_count_threshold:
                                        self.MOVE_LStick(dir1,dir2,dir3,dir4,3,"RELOAD")
                                    elif target_count>target_count_threshold2:
                                        self.MOVE_LStick(dir1,dir2,dir3,dir4,4,"RELOAD")
                                    break
                        target_marker_count+=1
                    elif target_marker_count>2:
                        target_marker_count=0
                    else:
                        self.MOVE_SEE(action = "",in_see_r=see_r)
                else:
                    target_marker_count=0
                    self.MOVE_SEE(action = "",in_see_r=see_r)
            self.ZL_ACTION("")
            count=(count + 1) % 4
            
            if not self.image_check("TEXT_BLACK_COMMENT"):
                if no_target_count>no_target_count_threshold:
                    self.MOVE_LStick(dir1,dir2,dir3,dir4,2,"RELOAD")
                elif target_count>target_count_threshold2:
                    self.MOVE_LStick(dir1,dir2,dir3,dir4,1,"RELOAD")
                #self.MOVE_SEE(action = "END",in_see_r=see_r)
                self.wait(0.1)

            elif self.image_check("TEXT_BLACK_COMMENT"):
                no_target_count=0
                no_target_count=target_count_threshold2
                self.MOVE_LStick(dir1,dir2,dir3,dir4,1,"END")
                    
            if self.image_check("FIELD_W"):
                self.etc_sendCommand("Lbutton_up")

            if self.image_check("TEXT_BLACK_COMMENT"):
                if nofiled==0:
                    nofiled=1
                    battle_count+=1
                    Cp_mode=(Cp_mode+1)%2#Cpのモード切替
                    print(f'BATTLE_COUNT::{battle_count}')
                no_target_count=0
                no_target_count=target_count_threshold2
                self.MOVE_LStick(dir1,dir2,1,dir3,dir4,"END")
                self.wait(1.0)
                if self.image_check("2_SELECT"):
                    self.wait(1.0)
                    if self.image_check("2_SELECT_TUTORIAL"):
                        self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1) 
                    else:
                        if not (self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W")):
                            self.etc_sendCommand("Lbutton_down")
                            self.wait(1.0)
                        self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)  
                elif self.image_check("3_SELECT"):
                    self.wait(1.0)
                    if self.image_check("3_SELECT_SELECT"):
                        self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    else:
                        if not (self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W")):
                            self.etc_sendCommand("Lbutton_down")
                            self.wait(1.0)
                        self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                else:
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                     
            elif self.image_check("TEXT_GREEN_COMMENT"):
                self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="1_SELECT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER")

            elif self.image_check("2_SELECT"):
                self.MOVE_LStick(dir1,dir2,dir3,dir4,1,"END")
                self.wait(1.0)
                if self.image_check("2_SELECT_TUTORIAL"):
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1) 
                else:
                    if not (self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W")):
                        self.etc_sendCommand("Lbutton_down")
                        self.wait(1.0)
                    self.wait(1.0)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)  
            elif self.image_check("3_SELECT"):
                self.MOVE_LStick(dir1,dir2,dir3,dir4,1,"END")
                self.wait(1.0)
                if self.image_check("3_SELECT_SELECT"):
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                else:
                    if not (self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W")):
                        self.etc_sendCommand("Lbutton_down")
                        self.wait(1.0)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)

            self.wait(0.5)

    def ZL_ACTION(self,action = "RELOAD",lockonflg=1):
        if action != "END":
            if lockonflg == 0:
                if self.ZL_state == 1:
                    self.keys.inputEnd(Button.ZL)
                    self.ZL_state = 0
                return
            if self.ZL_state == 0:
                self.keys.input(Button.ZL)
                self.ZL_state = 1
            else:
                self.keys.inputEnd(Button.ZL)
                #間隔をあけないとロックオンがオンにならない？
                self.wait(0.1)#self.wait(self.SLEEPLIST[2][2])
                self.keys.input(Button.ZL)
                self.ZL_state = 1
        elif action == "END" and self.ZL_state == 1:
            self.keys.inputEnd(Button.ZL)
            self.ZL_state = 0
            
    def battle_coCp_noloop(self,Xaction=0,Aaction=0,Yaction=0,Baction=0,lockon_endskip=0,battle_mode=0):
        if battle_mode==0 and self.image_check("SELECT"):
            self.etc_sendCommand("Lbutton_up")
        if battle_mode==1 and self.image_check("FIELD_W"):
            self.etc_sendCommand("Lbutton_up")
        self.ZL_ACTION("")
        for i in range(3):
            if Xaction==1:
                self.pressRep(Button.X, repeat=1, duration=0.04, wait=0.0, interval=0.1)
            if Aaction==1:
                self.pressRep(Button.A, repeat=1, duration=0.04, wait=0.0, interval=0.1)
            if Yaction==1:
                self.pressRep(Button.Y, repeat=1, duration=0.04, wait=0.0, interval=0.1)
            if Baction==1:
                self.pressRep(Button.B, repeat=1, duration=0.04, wait=0.0, interval=0.1)
        if lockon_endskip==0:
            self.ZL_ACTION("END")
            
    def battle_Cp_loop(self,Xaction=0,Aaction=0,Yaction=0,Baction=0,lockon_endskip=0,get_chanceicon4=0,mode=0,battle_mode=0,Cp_low_check=0):
        noCp_count=0
        target_marker=1
        while True:
            print(f'noCp_count = {noCp_count} mode = {mode} battle_mode = {battle_mode}')
            self.checkIfAlive()
            if battle_mode==0 and self.image_check("SELECT"):
                self.etc_sendCommand("Lbutton_up")
            elif battle_mode==1 and self.image_check("FIELD_W"):
                self.etc_sendCommand("Lbutton_up")
                
            self.ZL_ACTION("")
            
            for i in range(5):
                #バトル中チェック チェックできない場合は、一旦抜ける
                if mode==0 and (self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE") or self.image_check("C+")):
                    
                    if get_chanceicon4==1 and self.image_check("GETCHANCE_ICON4"):
                        self.get_pokemon()
                    if self.image_check("C+"):
                        noCp_count=0
                        if Xaction==1:
                            self.pressRep(Button.X, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                        if Aaction==1:
                            self.pressRep(Button.A, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                        if Yaction==1:
                            self.pressRep(Button.Y, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                        if Baction==1:
                            self.pressRep(Button.B, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                        self.MOVE_SEE(action = "END",in_see_r=0.6)
                    elif (self.image_check("TARGET_LEFT_MID") or self.image_check("TARGET_RIGHT_MID") or self.image_check("TARGET_RIGHT_RIHGT_CHECK_MID") or self.image_check("TARGET_LEFT_RIHGT_CHECK_MID")):
                        if target_marker>=1:
                            self.MOVE_SEE(action = "END",in_see_r=0.6)
                            target_marker=0
                        else:
                            target_marker+=1
                            if noCp_count>=3:
                                self.MOVE_SEE(action = "",in_see_r=0.6)
                            print(f'noCp_count = {noCp_count} 1')
                            if self.image_check("ESCAPE"):
                                noCp_count+=1#ロックオンはできていないためカウントは行う
                    else:
                        if noCp_count>=3:
                            print(f'noCp_count = {noCp_count} 6')
                            self.MOVE_SEE(action = "",in_see_r=0.6)
                        print(f'noCp_count = {noCp_count} 2')
                        if self.image_check("ESCAPE"):
                            noCp_count+=1
                elif mode==1 and (self.image_check("EYE_CHECK_HIGH_POKE") or self.image_check("C+")):
                    if self.image_check("FIELD_W"):
                        self.etc_sendCommand("Lbutton_up")
                        
                    if get_chanceicon4==1 and self.image_check("GETCHANCE_ICON4"):
                        self.get_pokemon()
                    if self.image_check("C+"):
                        noCp_count=0
                        if Xaction==1:
                            self.pressRep(Button.X, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                        if Aaction==1:
                            self.pressRep(Button.A, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                        if Yaction==1:
                            self.pressRep(Button.Y, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                        if Baction==1:
                            self.pressRep(Button.B, repeat=1, duration=0.04, wait=0.0, interval=0.1)
                        self.MOVE_SEE(action = "END",in_see_r=0.6)
                    elif (self.image_check("TARGET_LEFT_MID") or self.image_check("TARGET_RIGHT_MID") or self.image_check("TARGET_RIGHT_RIHGT_CHECK_MID") or self.image_check("TARGET_LEFT_RIHGT_CHECK_MID")):
                        if target_marker>=1:
                            self.MOVE_SEE(action = "END",in_see_r=0.6)
                            target_marker=0
                        else:
                            target_marker+=1
                            if noCp_count>=3:
                                self.MOVE_SEE(action = "",in_see_r=0.6)
                            print(f'noCp_count = {noCp_count} 1')
                            if self.image_check("ESCAPE"):
                                noCp_count+=1#ロックオンはできていないためカウントは行う
                    else:
                        if noCp_count>=3:
                            print(f'noCp_count = {noCp_count} 5')
                            self.MOVE_SEE(action = "",in_see_r=0.6)
                        print(f'noCp_count = {noCp_count} 4')
                        if self.image_check("ESCAPE"):
                            noCp_count+=1
                else:
                    self.MOVE_SEE(action = "END",in_see_r=0.6)
                    if lockon_endskip==0:
                        self.ZL_ACTION("END")
                    print("return")
                    return True
                
            if lockon_endskip==0:
                self.ZL_ACTION("END")
        return True

    ######################################################
    # story_Template
    ######################################################
    def story_Template_battle_before(self,noprg_ret,prg_ret,green_check=0,no_filed=0,sleeptime=0.5):
        if self.image_check("TEXT_WHITE_COMMENT") or ((green_check==1) and (self.image_check("TEXT_GREEN_COMMENT"))):
            if no_filed==0:
                endpicture="FIELD_W"
                endpicture2="FIELD_BACK_W"
            else:
                endpicture="FALSE_RETURN"
                endpicture2="FALSE_RETURN"
                
            if self.renda_button(rendabutton="B",endpicture=endpicture,endpicture2=endpicture2,endpicture3="BATTLE_BALL_CHECK",endpicture4="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=sleeptime):
                self.wait(1.0)
                return prg_ret
        return noprg_ret

    def story_Template_battle_function(self,bkprg_ret,prg_ret,noprg_ret,Xaction=0,Aaction=0,Yaction=0,Baction=0,lockon_endskip=0,get_chanceicon4=0,noCp=0,markertype=0,battle_mode=0,sleeptime=0.5):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE"):
            if noCp==0:
                self.battle_Cp_loop(Xaction=Xaction,Aaction=Aaction,Yaction=Yaction,Baction=Baction,get_chanceicon4=get_chanceicon4,battle_mode=battle_mode)
            else:
                if get_chanceicon4==1 and self.image_check("GETCHANCE_ICON4"):
                    self.get_pokemon()
                self.battle_coCp_noloop(Xaction=Xaction,Aaction=Aaction,Yaction=Yaction,Baction=Baction,battle_mode=battle_mode)
    
        elif self.image_check("CHAT_MARKER"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return bkprg_ret
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            for i in range(10):
                self.wait(1.0)
                if not (self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE")):
                    if self.image_check("TEXT_BLACK_COMMENT"):
                        return bkprg_ret
        elif self.image_check("TEXT_GREEN_COMMENT"):
            return prg_ret
        elif self.image_check("TEXT_WHITE_COMMENT"):
            return prg_ret
        elif self.image_check("COIN_ICON"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return prg_ret
        elif self.image_check("COIN_ICON"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return noprg_ret
        
        if not (self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE")):
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                if markertype==0:
                    if self.markerdir("EVENT"):
                        self.press(Direction(Stick.LEFT,90), duration=0.1, wait=0.5)
                        return noprg_ret
                elif markertype==1:
                    if self.markerdir("SIDE_MARKER"):
                        self.press(Direction(Stick.LEFT,90), duration=0.1, wait=0.5)
                        return noprg_ret
                else:
                    print("w3er")
                    return noprg_ret
            elif self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="COIN_ICON",endpicture3="BATTLE_BALL_CHECK",endpicture4="ESCAPE",endpicture5="TEXT_WHITE_COMMENT",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=sleeptime):
                return noprg_ret
        #elif self.image_check("EVENT_MARKER_CENTER"):
        #    self.press(Direction(Stick.LEFT,90), duration=0.1, wait=0.5)
        #    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
        #    return bkprg_ret

        return noprg_ret
    
    def story_Template_battle_after(self,bkprg_ret,prg_ret,selected_pic="RETURN FALSE",selected_target=0,sleeptime=0.5):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="BATTLE_BALL_CHECK",endpicture3="ESCAPE",endpicture4=selected_pic,sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=sleeptime):
            for i in range(10):
                self.wait(0.5)
                if (self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE")):
                    return bkprg_ret
                elif self.image_check(selected_pic):
                    self.wait(1.0)
                    for i in range(selected_target):
                        self.etc_sendCommand("Lbutton_down")
                        self.wait(0.5)
                    if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=sleeptime):
                        return prg_ret
            return prg_ret
        
    
    def story_Template_Comment_Out(self,substitute=0,green_check=1,black_check=1,selected_pic="RETURN FALSE",selected_target=0,sleeptime=0.5):
        selected_out_check=0
        #基本的にフィールドは以下でチェックするが、場所によって誤検知する場合がある。
        endpicture4="FIELD_W"
        endpicture5="FIELD_BACK_W"
        endpicture6="RETURN FALSE"
        #コメントチェックができるまでループ
        for i in range(10):
            if (self.image_check("TEXT_WHITE_COMMENT") or ((green_check==1) and (self.image_check("TEXT_GREEN_COMMENT"))) or ((black_check==1) and (self.image_check("TEXT_BLACK_COMMENT")))):
                break
            self.wait(0.5)
            
        #コメントチェック待ちをおこなっても検知ができなかった場合は、False判定とする。
        if (not (self.image_check("TEXT_WHITE_COMMENT") or ((green_check==1) and (self.image_check("TEXT_GREEN_COMMENT"))) or ((black_check==1) and (self.image_check("TEXT_BLACK_COMMENT"))))):
            return False
            
        while True:
            self.checkIfAlive()
            if self.renda_button(rendabutton="B",
                                 endpicture="BATTLE_BALL_CHECK",
                                 endpicture2="ESCAPE",
                                 endpicture3=selected_pic,
                                 endpicture4=endpicture4,
                                 endpicture5=endpicture5,
                                 endpicture6=endpicture6,
                                 sub_button="A",sub_picture="TEXT_BLACK_COMMENT",
                                 sub2_button="A",sub2_picture="2_SELECT",
                                 sub3_button="A",sub3_picture="3_SELECT",
                                 sub4_button="A",sub4_picture="4_SELECT",
                                 sub5_button="A",sub5_picture="HELP_MARKER",
                                 sub6_button="A",sub6_picture="MORNING",
                                 sub7_button="A",sub7_picture="NIGHT",
                                 sleeptime=sleeptime):
                selected_out_check=0
                for i in range(10):
                    self.wait(0.5)
                    if self.image_check(selected_pic):
                        selected_out_check=1
                        self.wait(1.0)
                        for i in range(selected_target):
                            self.etc_sendCommand("Lbutton_down")
                            self.wait(0.5)
                        self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                        break
                    
                    elif ((self.image_check("TEXT_WHITE_COMMENT") or ((green_check==1) and (self.image_check("TEXT_GREEN_COMMENT"))) or ((black_check==1) and (self.image_check("TEXT_BLACK_COMMENT")))) and (self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"))):
                        self.wait(0.5)
                        #選択肢チェックのタイミングがずれたようにフォローする
                        if self.image_check(selected_pic):
                            selected_out_check=1
                            self.wait(1.0)
                            for i in range(selected_target):
                                self.etc_sendCommand("Lbutton_down")
                                self.wait(0.5)
                            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                            break
                        else:
                            self.pressRep(Button.B, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            #選択肢処理を行っている場合は再度ボタン連打を再開する。
            if selected_out_check==1:
                selected_out_check=0
                continue
            self.wait(0.5)
            if (self.image_check("TEXT_WHITE_COMMENT") or ((green_check==1) and (self.image_check("TEXT_GREEN_COMMENT"))) or ((black_check==1) and (self.image_check("TEXT_BLACK_COMMENT")))):
                # 下記処理は戦闘不能となっている場合に実施すると抜けられなくなるため、回復などが前提にある場合でなければ使用しないこと
                if substitute==1:
                    endpicture4="WANINOKO_ICON"
                    endpicture5="ODAIRU_ICON"
                    endpicture6="ABSOL_ICON"
            elif self.image_check("MORNING") or self.image_check("NIGHT"):
                self.pressRep(Button.A, repeat=5, duration=0.15, wait=0.5, interval=0.1)
            else:
                break
        return True
        
    ######################################################
    # story_Template
    ###################################################### 
    def get_pokemon(self):
        self.ZL_ACTION("")
        self.wait(0.1)
        self.keys.input(Button.ZR)
        self.wait(0.15)
        self.keys.inputEnd(Button.ZR)
        self.wait(0.1)
        self.ZL_ACTION("END")
        
    def ball_change(self,type=0):

        for i in range(20):
            self.keys.input(Button.ZR)
            self.wait(2.0)
            if type==0 and self.image_check("M_BALL_ICON"):
                self.pressRep(Button.B, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                self.wait(1.0)
                self.keys.inputEnd(Button.ZR)
                return True
            elif type==2 and self.image_check("H_BALL_ICON"):
                self.pressRep(Button.B, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                self.wait(1.0)
                self.keys.inputEnd(Button.ZR)
                return True
            else:
                self.wait(1.0)
                self.etc_sendCommand("Lbutton_left")
                self.wait(1.0)
            self.pressRep(Button.B, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            self.keys.inputEnd(Button.ZR)
            self.wait(2.0)


        return False
    
    def EventSkip_plus(self):
        for i in range(3):
            self.etc_sendCommand("plusbutton")
            self.wait(0.1)
            self.etc_sendCommand("plusbutton_push")
            self.wait(3.0)
            self.etc_sendCommand("plusbutton_release")
    
    def markerdir(self,type,nofiled=False):
        if type == "EVENT":
            center = "EVENT_MARKER_CENTER"
            center_wide = "EVENT_MARKER_CENTER_WIDE"
            left = "EVENT_MARKER_LEFT_WIDE"
            right = "EVENT_MARKER_RIGHT_WIDE"
        elif type == "PIN":
            center = "PIN_MARKER_CENTER"
            center_wide = "PIN_MARKER_CENTER_WIDE"
            left = "PIN_MARKER_LEFT_WIDE"
            right = "PIN_MARKER_RIGHT_WIDE"
        elif type == "SIDE_MARKER":
            center = "SIDE_MARKER_CENTER"
            center_wide = "SIDE_MARKER_CENTER_WIDE"
            left = "SIDE_MARKER_LEFT_WIDE"
            right = "SIDE_MARKER_RIGHT_WIDE"
        else:
            return False
        
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W") or nofiled:
            if self.image_check(center):
                return True
            elif self.image_check(left):
                if self.image_check(center_wide):
                    self.press(Direction(Stick.RIGHT,180,0.3), duration=0.01, wait=0.0)
                else:
                    self.press(Direction(Stick.RIGHT,180), duration=0.01, wait=0.0)
            elif self.image_check(right):
                if self.image_check(center_wide):
                    self.press(Direction(Stick.RIGHT,0,0.3), duration=0.01, wait=0.0)
                else:
                    self.press(Direction(Stick.RIGHT,0), duration=0.01, wait=0.0)
            else:
                self.press(Direction(Stick.RIGHT,180), duration=0.3, wait=0.0)
            self.wait(0.1)
        return False

    def isContainTemplateUltra(self,         
                template_path ='img_crop.png',
                threshold = 0.7,
                use_gray = True,
                show_value = True,
                show_position = True,
                show_only_true_rect  = False,
                ms  = 2000,
                crop = [400,400,1280,710],
                crop_template  = [], 
                show_image = False,
                color  = ["blue", "red", "orange"],
        ):
        
        if show_image:
            self.imshow_name = f'{template_path}_pokecon_img'
            print(self.imshow_name)
            if window_acquire(Window_name=self.imshow_name,log=False,front_win=False) is None:
                while not window_acquire(Window_name=f'{self.imshow_name}',log=False,front_win=False) is None:
                    self.wait(0.1)
                # print('画像を表示します')
                self.thevent = threading.Event()
                if type(template_path) == str:
                    self.show_img_thread = threading.Thread(target=self.cv2imshow, args=(f'{template_path}',f'{self.template_path_name}{template_path}',))
                else:
                    self.show_img_thread = threading.Thread(target=self.cv2imshow, args=(f'{template_path}',template_path,))
                
                self.show_img_thread.start()
        
        ret = self.isContainTemplate(
            template_path =template_path, # 画像名またはbinary
            threshold = threshold,
            use_gray = use_gray,
            show_value = show_value,
            show_position = show_position,
            show_only_true_rect  = show_only_true_rect, # Trueが返ってきたときのみに枠表示
            ms  = ms, # 枠表示時間[ms]
            crop = crop, # [左上x,左上y,右下x,右下y]
            crop_template  = crop_template, # テンプレート画像のトリミング
            show_image = False, # 画像を表示する。処理は一時停止する。
            color  = color, # 判定True色, 判定False色, crop範囲色
        )
        
        if ret:
            self.imshow_end = True

        return ret
    
    def isContainTemplateUltra_get_max_val(self,         
                template_path ='img_crop.png',
                threshold = 0.7,
                use_gray = True,
                show_value = True,
                show_position = True,
                show_only_true_rect  = False,
                ms  = 2000,
                crop = [400,400,1280,710],
                crop_template  = [], 
                show_image = False,
                color  = ["blue", "red", "orange"],
                get_max_val = False,
        ):
        #max_val取得用
        max_val=0
        
        if show_image:
            self.imshow_name = f'{template_path}_pokecon_img'
            print(self.imshow_name)
            if window_acquire(Window_name=self.imshow_name,log=False,front_win=False) is None:
                while not window_acquire(Window_name=f'{self.imshow_name}',log=False,front_win=False) is None:
                    self.wait(0.1)
                # print('画像を表示します')
                self.thevent = threading.Event()
                if type(template_path) == str:
                    self.show_img_thread = threading.Thread(target=self.cv2imshow, args=(f'{template_path}',f'{self.template_path_name}{template_path}',))
                else:
                    self.show_img_thread = threading.Thread(target=self.cv2imshow, args=(f'{template_path}',template_path,))
                
                self.show_img_thread.start()
        
        if (not get_max_val or (self.TESTADDCODE==0)):
        
            ret = self.isContainTemplate(
                template_path =template_path, # 画像名またはbinary
                threshold = threshold,
                use_gray = use_gray,
                show_value = show_value,
                show_position = show_position,
                show_only_true_rect  = show_only_true_rect, # Trueが返ってきたときのみに枠表示
                ms  = ms, # 枠表示時間[ms]
                crop = crop, # [左上x,左上y,右下x,右下y]
                crop_template  = crop_template, # テンプレート画像のトリミング
                show_image = False, # 画像を表示する。処理は一時停止する。
                color  = color, # 判定True色, 判定False色, crop範囲色
            )
        else:
            #max_val返却用
            ret,max_val = self.isContainTemplate_get_max_val(
                template_path =template_path, # 画像名またはbinary
                threshold = threshold,
                use_gray = use_gray,
                show_value = show_value,
                show_position = show_position,
                show_only_true_rect  = show_only_true_rect, # Trueが返ってきたときのみに枠表示
                ms  = ms, # 枠表示時間[ms]
                crop = crop, # [左上x,左上y,右下x,右下y]
                crop_template  = crop_template, # テンプレート画像のトリミング
                show_image = False, # 画像を表示する。処理は一時停止する。
                color  = color, # 判定True色, 判定False色, crop範囲色
            )

        if ret:
            self.imshow_end = True

        if (not get_max_val):
            return ret
        else:
            return ret,max_val
        

######################################################
# ZA_battle_infi_Base
######################################################
    def ZA_battle_infi_main(self):
        
        while True:
            
            self.za_infi_main_current_state = self.STATE_ZA_INFI_MAIN_FUNCTION[self.za_infi_main_current_state]()
            self.wait(self.SLEEPLIST[9][2])
            self.out_str = (
                f'----------------------------'
                f'\n STATE_MAIN_FUNCTION   :: {self.za_infi_main_current_state}'
                f'\n'
                f'\n STATE_BENCH_FUNCTION  :: {self.bench_current_state}'
                f'\n STATE_BATTLE_FUNCTION :: {self.battle_current_state}'
                f'\n STATE_QUASAR_FUNCTION :: {self.quasar_current_state}'
                f'\n battlecount::{self.battlecount}'
                f'\n battle_step::{self.battle_step}'      
                f'\n chicketmaxflag::{self.chicketmaxflag}'
                f'\n ZL_state::{self.ZL_state}'  
                f'\n'  
                f'\n ZONECOUNT'
                f'\n[ 1 :{self.zonemisscount[0]}/{self.zonecount[0]}] '
                f'[ 2 :{self.zonemisscount[1]}/{self.zonecount[1]}] '
                f'[ 3 :{self.zonemisscount[2]}/{self.zonecount[2]}] '
                f'[ 4 :{self.zonemisscount[3]}/{self.zonecount[3]}] '
                f'[ 5 :{self.zonemisscount[4]}/{self.zonecount[4]}] '
                f'[ 6 :{self.zonemisscount[5]}/{self.zonecount[5]}] '
                f'\n[ 7 :{self.zonemisscount[6]}/{self.zonecount[6]}] '
                f'[ 8 :{self.zonemisscount[7]}/{self.zonecount[7]}] '
                f'[ 9 :{self.zonemisscount[8]}/{self.zonecount[8]}] '
                f'[10 :{self.zonemisscount[9]}/{self.zonecount[9]}] '
                f'[11 :{self.zonemisscount[10]}/{self.zonecount[10]}] '
                f'[12 :{self.zonemisscount[11]}/{self.zonecount[11]}]'
                f'\n'  
                f'\n QUASAR_LOSE_COUNT::{self.quasarlosecount}/{self.quasarcount}'
                f'\n battle_escape_count::{self.battleescapecount}'
                f'\n inactioncount::{self.inactioncount}'
                f'\n timechangemiss_count::{self.changetimemisscount}/{self.changetimecount}'
                f'\n'
                f' target_maker low:{self.target_end_low_count}/{self.target_start_low_count} mid:{self.target_end_mid_count}/{self.target_start_mid_count} normal:{self.target_end_count}/{self.target_start_count}\n'
                f' quasar_target_maker low:{self.quasar_target_end_low_count}/{self.quasar_target_start_low_count} mid:{self.quasar_target_end_mid_count}/{self.quasar_target_start_mid_count} normal:{self.quasar_target_end_count}/{self.quasar_target_start_count}\n'
                f' quasar_battle_display :{self.quasar_battle_display_end_count}/{self.quasar_battle_display_start_count}\n'
                f' battlemarker_skipcount {self.battlemarker_skipcount}/{self.battlemarker_skipcount_threshold}\n'
                f'\n'
                f'以下はTESTCODE=1でチェック {self.TESTADDCODE} ※PythonCommandBaseの編集が必要なため0とすること\n'  
                f'--------[ 50][ 55][ 60][ 65][ 70][ 75][ 80][ 85][ 90][ 95][100]\n'
                f'[left ::'
                f'[{self.target_left_max_val_list[0]:03d}]'
                f'[{self.target_left_max_val_list[1]:03d}]'
                f'[{self.target_left_max_val_list[2]:03d}]'
                f'[{self.target_left_max_val_list[3]:03d}]'
                f'[{self.target_left_max_val_list[4]:03d}]'
                f'[{self.target_left_max_val_list[5]:03d}]'
                f'[{self.target_left_max_val_list[6]:03d}]'
                f'[{self.target_left_max_val_list[7]:03d}]'
                f'[{self.target_left_max_val_list[8]:03d}]'
                f'[{self.target_left_max_val_list[9]:03d}]'
                f'[{self.target_left_max_val_list[10]:03d}]'
                f']\n'
                f'[right::'
                f'[{self.target_right_max_val_list[0]:03d}]'
                f'[{self.target_right_max_val_list[1]:03d}]'
                f'[{self.target_right_max_val_list[2]:03d}]'
                f'[{self.target_right_max_val_list[3]:03d}]'
                f'[{self.target_right_max_val_list[4]:03d}]'
                f'[{self.target_right_max_val_list[5]:03d}]'
                f'[{self.target_right_max_val_list[6]:03d}]'
                f'[{self.target_right_max_val_list[7]:03d}]'
                f'[{self.target_right_max_val_list[8]:03d}]'
                f'[{self.target_right_max_val_list[9]:03d}]'
                f'[{self.target_right_max_val_list[10]:03d}]'
                f']\n'
                f'\n----------------------------'
                )

            self.print_tb("d"); self.print_t(f'{self.out_str}')
            self.checkIfAlive()
        return True
     
    ######################################################
    # MAIN FUNCTION
    ######################################################  
    def za_infi_main_start(self):
        self.load_zones()
        self.no_Cplus=0      
        if self.fastread:
            self.load_sleeps()
        self.fastread = False
        #print(f'{self.SLEEPLIST}')
        return "ZA_INFI_MAIN_BENCH"
    
    def za_infi_main_bench(self):
        self.bench_current_state = self.STATE_BENCH_FUNCTION[self.bench_current_state]()
        if self.bench_current_state == "BATTLE_RETURN":
            self.bench_current_state="BENCH_START"
            self.battle_current_state="BATTLE_MOVE"
            return "ZA_INFI_MAIN_BATTLE_LOOP"
        elif self.bench_current_state == "BENCH_START":
            if self.chicketmaxflag == 2:
                return "ZA_INFI_QUASAR_LOOP"
            else:
                return "ZA_INFI_MAIN_BATTLE_LOOP"
        else:
            return "ZA_INFI_MAIN_BENCH"
        
    def za_infi_main_battle_loop(self):
        self.battle_current_state = self.STATE_BATTLE_FUNCTION[self.battle_current_state]()
        
        if self.battle_current_state == "BATTLE_START":
            return "ZA_INFI_MAIN_END"
        else:
            return "ZA_INFI_MAIN_BATTLE_LOOP"

    def za_infi_main_end(self):
        return "ZA_INFI_MAIN_START"
    
    def za_infi_quasar_loop(self):
        self.quasar_current_state = self.STATE_QUASAR_FUNCTION[self.quasar_current_state]()
        if self.quasar_current_state == "QUASAR_START":
            return "ZA_INFI_MAIN_END"
        else:
            return "ZA_INFI_QUASAR_LOOP"
######################################################
# ZA_battle_infi_Base_End
######################################################

######################################################
# 具体機能実装 
######################################################
    def ZA_story_main(self):
        
        while True:
            
            self.main_current_state = self.STATE_MAIN_FUNCTION[self.main_current_state]()
            self.wait(0.1)
            self.out_str = (
                f'----------------------------'
                f'\n STATE_MAIN_FUNCTION   :: {self.main_current_state}'
                f'\n'
                f'\n STATE_1_STORY_FUNCTION   :: {self._1_story_current_state}'
                f'\n STATE_2_STORY_FUNCTION   :: {self._2_story_current_state}'
                f'\n STATE_3_STORY_FUNCTION   :: {self._3_story_current_state}'
                f'\n STATE_4_STORY_FUNCTION   :: {self._4_story_current_state}'
                f'\n STATE_5_STORY_FUNCTION   :: {self._5_story_current_state}'
                f'\n STATE_6_STORY_FUNCTION   :: {self._6_story_current_state}'
                f'\n STATE_7_STORY_FUNCTION   :: {self._7_story_current_state}'
                f'\n STATE_8_STORY_FUNCTION   :: {self._8_story_current_state}'
                f'\n'
                f'\n ### STATE_2_VAR ###'
                f'\n BATTLE_COUNT :: {self._2_story_restaurant_dohutsu_battle_count}'
                f'\n'
                f'\n WHITE_CHECK :: {self._2_story_restaurant_dohutsu_white_check}'
                f'\n BLACK_CHECK  :: {self._2_story_restaurant_dohutsu_black_check}'
                f'\n'
                f'\n STATE_COMMON_SKILL_CHANGE_FUNCTION   :: {self.common_skill_change_current_state}'
                f'\n STATE_COMMON_BOX_CHANGE_FUNCTION   :: {self.common_box_change_current_state}'
                f'\n STATE_COMMON_ITEM_GIVE_FUNCTION   :: {self.common_item_give_current_state}'
                f'\n----------------------------'
                )
            

            self.print_tb("d"); self.print_t(f'{self.out_str}')
            self.checkIfAlive()
        return True   
    
    ######################################################
    # MAIN_STATE_INIT (引継ぎ実行用)
    ######################################################
    def main_state_init(self):
        if  self.main_current_state_init=="":
            return "MAIN_0_START"
        elif  self.main_current_state_init=="MAIN_1_Z_LANK":
            self._1_story_current_state=self._1_story_current_state_init
            return "MAIN_1_Z_LANK"
        elif  self.main_current_state_init=="MAIN_2_Y_V_LANK":
            self._2_story_current_state=self._2_story_current_state_init
            return "MAIN_2_Y_V_LANK"
        elif  self.main_current_state_init=="MAIN_3_F_LANK":
            self._3_story_current_state=self._3_story_current_state_init
            return "MAIN_3_F_LANK"
        elif  self.main_current_state_init=="MAIN_4_E_LANK":
            self._4_story_current_state=self._4_story_current_state_init
            return "MAIN_4_E_LANK"
        elif  self.main_current_state_init=="MAIN_5_D_LANK":
            self._5_story_current_state=self._5_story_current_state_init
            return "MAIN_5_D_LANK"
        elif  self.main_current_state_init=="MAIN_6_C_LANK":
            self._6_story_current_state=self._6_story_current_state_init
            return "MAIN_6_C_LANK"
        elif  self.main_current_state_init=="MAIN_7_B_LANK":
            self._7_story_current_state=self._7_story_current_state_init
            return "MAIN_7_B_LANK"
        elif  self.main_current_state_init=="MAIN_8_STORY_LAST":
            self._8_story_current_state=self._8_story_current_state_init
            return "MAIN_8_STORY_LAST"
        else:
            return self.main_current_state_init
        
    ######################################################
    # MAIN_0_START FUNCTION
    ######################################################
    def main_0_start(self):
        if self.check_picture==1:
            if self.image_check("PROFILE",1):
                print("PROFILE")
            if self.image_check("STARTBTN_SELECT",1):
                print("STARTBTN_SELECT")
            
            self.wait(1.0)
        else:
            if self.image_check("PROFILE"):
                if self.image_check("STARTBTN_SELECT"):
                    self.pressRep(Button.A, repeat=20, duration=0.15, wait=0.5, interval=0.1)
                    self.wait(0.1)
                    self.EventSkip_plus()
                    return "MAIN_1_Z_LANK"
        return "MAIN_0_START"
    
    ######################################################
    # MAIN_1_Z_LANK FUNCTION
    ######################################################
    def main_1_z_lank(self):
        self._1_story_current_state = self.STATE_1_STORY_FUNCTION[self._1_story_current_state]()
        if self._1_story_current_state == "1_STORY_END":
            return "MAIN_2_Y_V_LANK"
        else:
            return "MAIN_1_Z_LANK"
    
    ######################################################
    # MAIN_2_Y_V_LANK FUNCTION
    ######################################################
    def main_2_y_v_lank(self):
        self._2_story_current_state = self.STATE_2_STORY_FUNCTION[self._2_story_current_state]()
        if self._2_story_current_state == "2_STORY_END":
            return "MAIN_3_F_LANK"
        else:
            return "MAIN_2_Y_V_LANK"

    ######################################################
    # MAIN_3_F_LANK FUNCTION
    ######################################################
    def main_3_f_lank(self):
        self._3_story_current_state = self.STATE_3_STORY_FUNCTION[self._3_story_current_state]()
        if self._3_story_current_state == "3_STORY_END":
            return "MAIN_4_E_LANK"
        else:
            return "MAIN_3_F_LANK"
        
    ######################################################
    # MAIN_4_E_LANK FUNCTION
    ######################################################
    def main_4_e_lank(self):
        self._4_story_current_state = self.STATE_4_STORY_FUNCTION[self._4_story_current_state]()
        if self._4_story_current_state == "4_STORY_END":
            return "MAIN_5_D_LANK"
        else:
            return "MAIN_4_E_LANK"
        
    ######################################################
    # MAIN_5_D_LANK FUNCTION
    ######################################################
    def main_5_d_lank(self):
        self._5_story_current_state = self.STATE_5_STORY_FUNCTION[self._5_story_current_state]()
        if self._5_story_current_state == "5_STORY_END":
            return "MAIN_6_C_LANK"
        else:
            return "MAIN_5_D_LANK"
        
    ######################################################
    # MAIN_6_C_LANK FUNCTION
    ######################################################
    def main_6_c_lank(self):
        self._6_story_current_state = self.STATE_6_STORY_FUNCTION[self._6_story_current_state]()
        if self._6_story_current_state == "6_STORY_END":
            return "MAIN_7_B_LANK"
        else:
            return "MAIN_6_C_LANK"
        
    ######################################################
    # MAIN_7_B_LANK FUNCTION
    ######################################################
    def main_7_b_lank(self):
        self._7_story_current_state = self.STATE_7_STORY_FUNCTION[self._7_story_current_state]()
        if self._7_story_current_state == "7_STORY_END":
            return "MAIN_8_STORY_LAST"
        else:
            return "MAIN_7_B_LANK"
        
    ######################################################
    # MAIN_8_STORY_LASTFUNCTION
    ######################################################
    def main_8_story_last(self):
        self._8_story_current_state = self.STATE_8_STORY_FUNCTION[self._8_story_current_state]()
        if self._8_story_current_state == "8_STORY_END":
            return "MAIN_STORY_END"
        else:
            return "MAIN_8_STORY_LAST"
        
    ######################################################
    # MAIN_STORY_END FUNCTION
    ######################################################
    def main_story_end(self):
        #一旦空
        return "MAIN_STORY_END"
        
        
    ######################################################
    # MAIN_1_Z_LANK SUB FUNCTION
    ######################################################
    def _1_story_start_check(self):
        if self.image_check("TEXT_BLACK_COMMENT"):
            return "1_STORY_TRAIN_OUT"  
        elif self.image_check("TEXT_TRAIN_OUT_COMMENT"):
            return "1_STORY_STATION_OUT"
        else:
            self.EventSkip_plus()
            return "1_STORY_START_CHECK"
        
    def _1_story_train_out(self):
        if self.check_picture==1:
            if self.image_check("TEXT_BLACK_COMMENT"):
                print("TEXT_BLACK_COMMENT")          
            self.wait(1.0)
        else:
            if self.image_check("TEXT_BLACK_COMMENT"):
                self.pressRep(Button.B, repeat=10, duration=0.15, wait=0.5, interval=0.1)
                return "1_STORY_STATION_OUT"
        return "1_STORY_TRAIN_OUT"  

    def _1_story_staition_out(self):
        ### AUTO_SAVE_POINT
        if self.check_picture==1:
            if self.image_check("TEXT_TRAIN_OUT_COMMENT"):
                print("TEXT_TRAIN_OUT_COMMENT")
            
            self.wait(1.0)
        else:
            if self.image_check("TEXT_TRAIN_OUT_COMMENT"):
                self.press(Direction(Stick.LEFT,80), duration=4.0, wait=1.0) # 位置調整
                self.press(Direction(Stick.LEFT,0), duration=9.6, wait=1.0) # 位置調整
                return "1_STORY_STATION_FRONT"

        return "1_STORY_STATION_OUT"
    
    def _1_story_staition_front(self):
        ### AUTO_SAVE_POINT
        if self.check_picture==1:
            if self.image_check("TEXT_STATION_LEAVE_COMMENT"):
                print("TEXT_STATION_LEAVE_COMMENT")
                
        else:
            if self.image_check("TEXT_WHITE_COMMENT"):
                if self.renda_button(rendabutton="B",endpicture="TEXT_STATION_LEAVE_COMMENT",sub_button="A",sub_picture="2_SELECT",event_picture="QUASAR_MOVIE_ICON"):
                    return "1_STORY_STATION_LEAVE_MOVE"
        
        return "1_STORY_STATION_FRONT"
        
    def _1_story_staition_leave_move(self):
        if self.check_picture==1:
            if self.image_check("TEXT_STATION_LEAVE_COMMENT"):
                print("TEXT_STATION_LEAVE_COMMENT")   
        else:
            if self.image_check("TEXT_STATION_LEAVE_COMMENT"):
                self.press(Direction(Stick.LEFT,90), duration=4.0, wait=1.0)
                self.press(Direction(Stick.LEFT,180), duration=4.4, wait=1.0)
                self.press(Direction(Stick.LEFT,90), duration=10.5, wait=1.0)
                self.press(Direction(Stick.LEFT,180), duration=6.0, wait=1.0)
                self.press(Direction(Stick.LEFT,60), duration=0.13, wait=1.0)
                self.press(Direction(Stick.LEFT,120), duration=6.0, wait=1.0)
                self.press(Direction(Stick.LEFT,240), duration=4.0, wait=1.0)
                self.press(Direction(Stick.LEFT,120), duration=6.0, wait=1.0)
                return "1_STORY_BAG_CHASE_END"
        return "1_STORY_STATION_LEAVE_MOVE"

    def _1_story_bag_chase_end(self):
        if self.check_picture==1:
            if self.image_check("TEXT_STATION_LEAVE_COMMENT"):
                print("TEXT_STATION_LEAVE_COMMENT") 
        else:
            if self.image_check("TEXT_WHITE_COMMENT"):
                if self.renda_button(rendabutton="B",endpicture="CHAT_MARKER",sub_button="A",sub_picture="2_SELECT"):
                    return "1_STORY_FARST_POKEMON_SELECT"
        return "1_STORY_BAG_CHASE_END"
    
    def _1_story_farst_pokemon_select(self):
        ### AUTO_SAVE_POINT
        if self.check_picture==1:
            if self.image_check("CHAT_MARKER"):
                print("CHAT_MARKER") 
            if self.image_check("HELP_MARKER"):
                print("HELP_MARKER") 
        else:
            if self.image_check("CHAT_MARKER"):
                self.press(Direction(Stick.LEFT,150), duration=0.7, wait=1.0)
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                if self.renda_button(rendabutton="B",endpicture="HELP_MARKER",sub_button="A",sub_picture="2_SELECT"):
                    return "1_STORY_FARST_BATTLE"
        return "1_STORY_FARST_POKEMON_SELECT"
    
    def _1_story_farst_battle(self):
        if self.check_picture==1:
            if self.image_check("HELP_MARKER"):
                print("HELP_MARKER") 
        else:
            if self.image_check("BATTLE_BALL_CHECK"):
                self.battle_coCp_noloop(Xaction=1,Aaction=1,Yaction=0,Baction=0)
            elif self.image_check("TEXT_WHITE_COMMENT"):
                return "1_STORY_FARST_BATTLE_END"
            elif self.image_check("HELP_MARKER"):
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
        return "1_STORY_FARST_BATTLE"
    
    def _1_story_farst_battle_end(self):
        if self.check_picture==1:
            if self.image_check("TEXT_WHITE_COMMENT"):
                print("TEXT_WHITE_COMMENT") 
        else:
            if self.image_check("TEXT_WHITE_COMMENT"):
                if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT"):
                    return "1_STORY_FARST_BATTLE_ZONE_MOVE1"
        return "1_STORY_FARST_BATTLE_END"
    
    def _1_story_farst_battle_zone_move1(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=3.8, wait=1.0)#4.0
            self.press(Direction(Stick.LEFT,0), duration=6.2, wait=1.0)
            self.press(Direction(Stick.LEFT,270), duration=4.0, wait=1.0)
            return "1_STORY_SECOND_BATTLE_START"
        return "1_STORY_FARST_BATTLE_ZONE_MOVE1"
    
    def _1_story_second_battle_start(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="BATTLE_BALL_CHECK",endpicture2="ESCAPE",sub_button="A",sub_picture="2_SELECT"):
                return "1_STORY_SECOND_BATTLE"
        return "1_STORY_SECOND_BATTLE_START"
    
    def _1_story_second_battle(self):

        if self.image_check("BATTLE_BALL_CHECK"):
            self.battle_coCp_noloop(Xaction=1,Aaction=1,Yaction=1,Baction=0)
        elif self.image_check("TEXT_WHITE_COMMENT"):
            return "1_STORY_SECOND_BATTLE_END"  
        return "1_STORY_SECOND_BATTLE"  
    
    def _1_story_second_battle_end(self):

        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT"):
                return "1_STORY_FARST_BATTLE_ZONE_MOVE2" 
        return "1_STORY_SECOND_BATTLE_END" 

    def _1_story_farst_battle_zone_move2(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.8, wait=1.0)
            self.press(Direction(Stick.LEFT,180), duration=4.2, wait=1.0)
            self.press(Direction(Stick.LEFT,90), duration=2.5, wait=1.0)
            self.wait(3.0)
            self.EventSkip_plus()
            return "1_STORY_FARST_MOVIE_END"
        return "1_STORY_FARST_BATTLE_ZONE_MOVE2"

    def _1_story_farst_movie_end(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT"):
                return "1_STORY_FARST_BATTLE_ZONE_MOVE3" 
        return "1_STORY_FARST_MOVIE_END"
        
    def _1_story_farst_battle_zone_move3(self):
        ### AUTO_SAVE_POINT
        if self.image_check("OUT_MARKER"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(2.0)
            return "1_STORY_FARST_BATTLE_ZONE_OUT"
        elif self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=6.0, wait=1.0)
            return "1_STORY_FARST_BATTLE_ZONE_MOVE3"
        return "1_STORY_FARST_BATTLE_ZONE_MOVE3"

    def _1_story_farst_battle_zone_out(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT"):
                return "1_STORY_FARST_BATTLE_ZONE_MOVE4" 
        return "1_STORY_FARST_BATTLE_ZONE_OUT"

    def _1_story_farst_battle_zone_move4(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,10), duration=8.0, wait=1.0)
            return "1_STORY_HOTEL_Z_ARRIVAL"
        return "1_STORY_FARST_BATTLE_ZONE_MOVE4"
    
    def _1_story_hote_z_arrival(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT"):
                return "1_STORY_HOTEL_Z_MOVE1"

        return "1_STORY_HOTEL_Z_ARRIVAL"

    def _1_story_hote_z_move1(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=5.0, wait=1.0)
            return "1_STORY_HOTEL_Z_MOVE2"
        return "1_STORY_HOTEL_Z_MOVE1"

    def _1_story_hote_z_move2(self):
        if self.image_check("IN_MARKER"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(2.0)
            return "1_STORY_HOTEL_Z_FAST_IN"
        return "1_STORY_HOTEL_Z_MOVE2"
    
    def _1_story_hote_z_fast_in(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT"):
                return "1_STORY_HOTEL_Z_MOVE3"
        return "1_STORY_HOTEL_Z_FAST_IN"
    
    def _1_story_hote_z_move3(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,95), duration=4.0, wait=1.0)
            self.press(Direction(Stick.LEFT,180), duration=0.1, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_AZ_CHAT"
        return "1_STORY_HOTEL_Z_MOVE3"
    
    def _1_story_az_chat(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="IN_ICON",sub_button="A",sub_picture="TEXT_BLACK_COMMENT"):
                return "1_STORY_HOTEL_Z_MOVE4"
        return "1_STORY_AZ_CHAT"
    
    def _1_story_hote_z_move4(self):
        if self.image_check("IN_ICON"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_FAST_ELEVATOR"
        return "1_STORY_HOTEL_Z_MOVE4"

    def _1_story_fast_elevator(self):
        if self.renda_button(rendabutton="B",endpicture="IN_ICON",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sleeptime=0.5):
            return "1_STORY_HOTEL_Z_MOVE5"
        return "1_STORY_FAST_ELEVATOR"
    
    def _1_story_hote_z_move5(self):
        if self.image_check("IN_ICON"):
            self.press(Direction(Stick.LEFT,100), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_HOTEL_Z_MOVE6"
        return "1_STORY_HOTEL_Z_MOVE5"

    def _1_story_hote_z_move6(self):
        if self.image_check("TEXT_BLACK_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="WANINOKO_ICON",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sleeptime=0.5):
                return "1_STORY_HOTEL_Z_MOVE7"

        return "1_STORY_HOTEL_Z_MOVE6"   
    
    def _1_story_hote_z_move7(self):
        ### AUTO_SAVE_POINT
        if self.image_check("WANINOKO_ICON"):
            self.press(Direction(Stick.LEFT,55), duration=1.1, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)

            return "1_STORY_HOTEL_Z_MOVE8" 
        return "1_STORY_HOTEL_Z_MOVE7"   
    
    def _1_story_hote_z_move8(self):
        if self.image_check("TEXT_BLACK_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="IN_ICON",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sleeptime=0.5):
                return "1_STORY_HOTEL_Z_MOVE9"

        return "1_STORY_HOTEL_Z_MOVE8"  
    
    def _1_story_hote_z_move9(self):
        ### AUTO_SAVE_POINT
        if self.image_check("IN_ICON"):
            self.press(Direction(Stick.LEFT,80), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_HOTEL_Z_MOVE10"
        return "1_STORY_HOTEL_Z_MOVE9" 
    
    def _1_story_hote_z_move10(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="IN_ICON",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sleeptime=0.5):
                return "1_STORY_HOTEL_Z_MOVE11"

        return "1_STORY_HOTEL_Z_MOVE10"
    
    def _1_story_hote_z_move11(self):
        ### AUTO_SAVE_POINT
        if self.image_check("IN_ICON"):
            self.press(Direction(Stick.LEFT,90), duration=2.4, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_HOTEL_Z_MOVE12"
        return "1_STORY_HOTEL_Z_MOVE11" 
    
    def _1_story_hote_z_move12(self):
        #左上のアイコンがバックアップ時に出ないため、小移動で休むアイコンが出るかで判断とする。
        if self.image_check("WANINOKO_ICON"):
            self.press(Direction(Stick.LEFT,100), duration=2.1, wait=1.0)

            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            # ロワイヤル画面でFILED判定してしまう場合があるため一旦代用でWANINOKO_ICONで判断
            if self.renda_button(rendabutton="B",endpicture="WANINOKO_ICON",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "1_STORY_HOTEL_Z_MOVE13" 

        return "1_STORY_HOTEL_Z_MOVE12" 
    
    def _1_story_hote_z_move13(self):
        ### AUTO_SAVE_POINT
        # 1_STORY_HOTEL_Z_MOVE12から予期せず飛んだ場合
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "1_STORY_HOTEL_Z_MOVE13" 
        elif self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=4.0, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_HOTEL_Z_MOVE14"
        return "1_STORY_HOTEL_Z_MOVE13"

    def _1_story_hote_z_move14(self):
        # 1_STORY_HOTEL_Z_MOVE12から予期せず飛んだ場合
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "1_STORY_HOTEL_Z_MOVE13" 
        elif self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.9, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_HOTEL_Z_MOVE15"
        return "1_STORY_HOTEL_Z_MOVE14"
    
    def _1_story_hote_z_move15(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="BATTLE_BALL_CHECK",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sleeptime=0.5):
                return "1_STORY_THIRD_BATTLE"
        return "1_STORY_HOTEL_Z_MOVE15"
    
    def _1_story_third_battle(self):
        if self.image_check("BATTLE_BALL_CHECK"):
            self.battle_coCp_noloop(Xaction=1,Aaction=1,Yaction=1,Baction=0)
        elif self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="BATTLE_BALL_CHECK",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER",sleeptime=0.5):
                for i in range(20):
                    if self.image_check("BATTLE_BALL_CHECK"):
                        return "1_STORY_THIRD_BATTLE"
                    elif self.image_check("TEXT_WHITE_COMMENT"):
                        self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="BATTLE_BALL_CHECK",sub_button="A",sub_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER")
                return "1_STORY_THIRD_BATTLE_END"
        return "1_STORY_THIRD_BATTLE"
    
    def _1_story_third_battle_end(self):
        ### AUTO_SAVE_POINT
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT"):
                return "1_STORY_OUT_HOTEL_Z_1"
        else:
            self.press(Direction(Stick.LEFT,90), duration=10.0, wait=1.0)    
        return "1_STORY_THIRD_BATTLE_END"
    
    def _1_story_out_hotel_z_1(self):
        ### AUTO_SAVE_POINT
        self.press(Direction(Stick.LEFT,90), duration=11.0, wait=1.0)
        for i in range(20):
            self.press(Direction(Stick.LEFT,0), duration=0.1, wait=1.0)
            if self.image_check("HASHIGO_ICON"):
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1) 
                return "1_STORY_OUT_HOTEL_Z_2"
        return "1_STORY_OUT_HOTEL_Z_2"
    
    def _1_story_out_hotel_z_2(self):
        self.press(Direction(Stick.LEFT,90), duration=7.0, wait=1.0)
        return "1_STORY_OUT_HOTEL_Z_3"
    
    def _1_story_out_hotel_z_3(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT"):
                return "1_STORY_OUT_HOTEL_Z_4"
        return "1_STORY_OUT_HOTEL_Z_3"
    
    def _1_story_out_hotel_z_4(self):
        ### AUTO_SAVE_POINT
        self.press(Direction(Stick.LEFT,90), duration=6.0, wait=1.0)
        return "1_STORY_OUT_HOTEL_Z_5"
    
    def _1_story_out_hotel_z_5(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT"):
                return "1_STORY_OUT_HOTEL_Z_6"
        return "1_STORY_OUT_HOTEL_Z_5"
    
    def _1_story_out_hotel_z_6(self):
        ### AUTO_SAVE_POINT
        self.press(Direction(Stick.LEFT,60), duration=5.2, wait=1.0)
        self.press(Direction(Stick.LEFT,153), duration=4.0, wait=1.0)
        self.wait(0.5)
        if self.image_check("CHAT_MARKER"):
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_7"
        
        self.press(Direction(Stick.LEFT,0), duration=0.1, wait=1.0)
        self.wait(0.5)
        self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
        return "1_STORY_OUT_HOTEL_Z_7"

    def _1_story_out_hotel_z_7(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT",sub2_button="A",sub2_picture="HELP_MARKER"):
                return "1_STORY_OUT_HOTEL_Z_8"

        return "1_STORY_OUT_HOTEL_Z_7"

    def _1_story_out_hotel_z_8(self):
        ### AUTO_SAVE_POINT
        self.press(Direction(Stick.LEFT,90), duration=14.0, wait=1.0)
        return "1_STORY_OUT_HOTEL_Z_9"
    
    def _1_story_out_hotel_z_9(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT",sub2_button="A",sub2_picture="HELP_MARKER"):
                return "1_STORY_WANINOKO_SKILL_CHANGE1"
        return "1_STORY_OUT_HOTEL_Z_9"
    
    def _1_story_waninoko_skill_change1(self):
        #ワニノコの水鉄砲をA技に、C+チェックできないとローリングが誤発動するパターンがあるため、AB技で戦えるようにする。
        ret = self.common_skill_change_function(1,"Y","B")
        #if self.common_skill_change_current_state
        if ret == "COMMON_SKILL_CHANGE_START":
            return "1_STORY_WANINOKO_SKILL_CHANGE2"
        else: 
            return "1_STORY_WANINOKO_SKILL_CHANGE1"

    def _1_story_waninoko_skill_change2(self):
        #ワニノコの水鉄砲をA技に、C+チェックできないとローリングが誤発動するパターンがあるため、AB技で戦えるようにする。
        ret = self.common_skill_change_function(1,"X","A")
        #if self.common_skill_change_current_state
        if ret == "COMMON_SKILL_CHANGE_START":
            return "1_STORY_OUT_HOTEL_Z_10"
        else: 
            return "1_STORY_WANINOKO_SKILL_CHANGE2"
    
    def _1_story_out_hotel_z_10(self):
        ### AUTO_SAVE_POINT
        self.press(Direction(Stick.LEFT,90), duration=5.0, wait=1.0)
        self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
        self.wait(0.5)
        return "1_STORY_OUT_HOTEL_Z_11"
    
    def _1_story_out_hotel_z_11(self):  
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER",sleeptime=0.5):
                return "1_STORY_OUT_HOTEL_Z_12"
        return "1_STORY_OUT_HOTEL_Z_11"
    
    def _1_story_out_hotel_z_12(self):
        self.get_pokemon()
        return "1_STORY_OUT_HOTEL_Z_13"
    
    def _1_story_out_hotel_z_13(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER",sleeptime=0.5):
                return "1_STORY_OUT_HOTEL_Z_14"

        return "1_STORY_OUT_HOTEL_Z_13"
    
    def _1_story_out_hotel_z_14(self):  
        self.get_pokemon()
        return "1_STORY_OUT_HOTEL_Z_15"
    
    def _1_story_out_hotel_z_15(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER",sleeptime=0.5):
                self._1_story_2nd_get_comment=0
                return "1_STORY_OUT_HOTEL_Z_16"

        return "1_STORY_OUT_HOTEL_Z_15"
    
    def _1_story_out_hotel_z_16(self):
        if self._1_story_2nd_get_comment==1:
            # ゲットチャンスコメントに妨害されるためコメントがでるまで以下で行わない。
            if self.image_check("GETCHANCE_ICON4"):
                self.get_pokemon()
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            if self.image_check("FIELD_W"):
                self.etc_sendCommand("Lbutton_up")
            self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1,lockon_endskip=1)
        elif self.image_check("TEXT_WHITE_COMMENT"):
            self.wait(0.1)
            if self.image_check("TEXT_2_GETCHANCE"):
                if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="HELP_MARKER"):
                    self.wait(0.1)
                    self.get_pokemon()
            elif self.image_check("TEXT_2_GET_SUCCESS"):
                if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="HELP_MARKER"):
                    self.ZL_ACTION("END")
                    return "1_STORY_OUT_HOTEL_Z_17" 
            else:
                self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="HELP_MARKER")
            self._1_story_2nd_get_comment=1
 
        return "1_STORY_OUT_HOTEL_Z_16"
        
    def _1_story_out_hotel_z_17(self):
        ### AUTO_SAVE_POINT
        #コフキムシを探索
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,60), duration=6.0, wait=1.0)
            self.press(Direction(Stick.LEFT,120), duration=0.1, wait=1.0)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_18" 
        return "1_STORY_OUT_HOTEL_Z_17"   
    
    def _1_story_out_hotel_z_18(self):
        if self.image_check("KOHUKI_ICON_GET4"):
            self.ZL_ACTION("END")
            
            #コフキムシは1体
            return "1_STORY_OUT_HOTEL_Z_19"
            #return "1_STORY_OUT_HOTEL_Z_18_1"
        elif self.image_check("GETCHANCE_ICON4"):
            self.get_pokemon()
            self.wait(3.0)
            for i in range(6):
                if self.image_check("KOHUKI_ICON_GET4"):
                    self.ZL_ACTION("END")
                    return "1_STORY_OUT_HOTEL_Z_19"
                elif self.image_check("EYE_CHECK"):
                    self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1,lockon_endskip=1)
                self.wait(1.0)
            #ゲット時に自動でセーブされてしまうため大体の位置を確定させたいため待機
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            if self.image_check("FIELD_W"):
                self.etc_sendCommand("Lbutton_up")
            self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1,lockon_endskip=1)
        return "1_STORY_OUT_HOTEL_Z_18" 

    def _1_story_out_hotel_z_18_1(self):
        ### AUTO_SAVE_POINT
        #コフキムシを探索
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=0.7, wait=1.0)
            return "1_STORY_OUT_HOTEL_Z_18_2" 
        return "1_STORY_OUT_HOTEL_Z_18_1"   
    
    def _1_story_out_hotel_z_18_2(self):
        if self.image_check("KOHUKI_ICON_GET4") and self.image_check("KOHUKI_ICON_GET5"):
            self.ZL_ACTION("END")
            return "1_STORY_OUT_HOTEL_Z_19"
        elif self.image_check("GETCHANCE_ICON4"):
            self.get_pokemon()
            self.wait(2.0)
            #ゲット時に自動でセーブされてしまうため大体の位置を確定させたいため待機
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            if self.image_check("FIELD_W"):
                self.etc_sendCommand("Lbutton_up")
            self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1,lockon_endskip=1)
        return "1_STORY_OUT_HOTEL_Z_18_2" 

    def _1_story_out_hotel_z_19(self):
        ### AUTO_SAVE_POINT
        if self.markerdir("EVENT"):
            return "1_STORY_OUT_HOTEL_Z_19_1" 
        else:
            return "1_STORY_OUT_HOTEL_Z_19"

    def _1_story_out_hotel_z_19_1(self):
        #メリープを探索
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,120), duration=4.0, wait=1.0)
            self.press(Direction(Stick.LEFT,70), duration=5.0, wait=1.0)
            self.press(Direction(Stick.LEFT,40), duration=7.0, wait=1.0)
            self.press(Direction(Stick.LEFT,280), duration=3.0, wait=1.0)
            self.press(Direction(Stick.LEFT,40), duration=3.0, wait=1.0)
            self.press(Direction(Stick.LEFT,220), duration=0.5, wait=1.0)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_20" 
        return "1_STORY_OUT_HOTEL_Z_19_1" 
    
    def _1_story_out_hotel_z_20(self):
        if self.image_check("MERIP_ICON_GET5"):
            self.ZL_ACTION("END")
            return "1_STORY_OUT_HOTEL_Z_20_1"
        elif self.image_check("GETCHANCE_ICON4"):
            self.wait(0.25)
            self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1,lockon_endskip=1)
            self.wait(0.25)
            self.get_pokemon()
            self.wait(0.25)
            #ゲット時に自動でセーブされてしまうため大体の位置を確定させたいため待機
            for i in range(6):
                if self.image_check("MERIP_ICON_GET5"):
                    self.ZL_ACTION("END")
                    return "1_STORY_OUT_HOTEL_Z_20_1"
                elif self.image_check("EYE_CHECK"):
                    self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1,lockon_endskip=1)
                self.wait(1.0)
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            if self.image_check("FIELD_W"):
                self.etc_sendCommand("Lbutton_up")
            if self.image_check("EYE_CHECK"):
                if self._1_story_out_hotel_z_20_not_eyecheck_count > 10:
                    self.press(Direction(Stick.RIGHT,0), duration=0.1, wait=1.0)
                    self._1_story_out_hotel_z_20_not_eyecheck_count=0
            else:
                self._1_story_out_hotel_z_20_not_eyecheck_count+=1
                
            self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1,lockon_endskip=1)
        return "1_STORY_OUT_HOTEL_Z_20" 
    
    def _1_story_out_hotel_z_20_1(self):
        if self.markerdir("EVENT"):
            return "1_STORY_OUT_HOTEL_Z_21" 
        else:
            return "1_STORY_OUT_HOTEL_Z_20_1"
        
    def _1_story_out_hotel_z_21(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            #方向が不明のため、出口右の隅にオーバーラン
            #self.press(Direction(Stick.LEFT,250), duration=5.0, wait=1.0)
            self.press(Direction(Stick.LEFT,10), duration=5.0, wait=1.0)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            if self.image_check("OUT_MARKER"):
                self.wait(0.1)
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                return "1_STORY_OUT_HOTEL_Z_22" 
            for i in range(5):
                self.press(Direction(Stick.LEFT,180), duration=0.3, wait=1.0)
                if self.image_check("OUT_MARKER"):
                    self.wait(0.1)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    return "1_STORY_OUT_HOTEL_Z_22"
            for i in range(20):
                self.press(Direction(Stick.LEFT,280), duration=0.2, wait=1.0)
                self.press(Direction(Stick.LEFT,180), duration=0.4, wait=1.0)
                if self.image_check("OUT_MARKER"):
                    self.wait(0.1)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    return "1_STORY_OUT_HOTEL_Z_22"
        return "1_STORY_OUT_HOTEL_Z_21" 
    
    def _1_story_out_hotel_z_22(self):
        if self.markerdir("EVENT"):
            return "1_STORY_OUT_HOTEL_Z_23" 
        else:
            return "1_STORY_OUT_HOTEL_Z_22"
        
    def _1_story_out_hotel_z_23(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            return "1_STORY_OUT_HOTEL_Z_24" 
        elif self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=10.0, wait=1.0)
        return "1_STORY_OUT_HOTEL_Z_23"
    
    def _1_story_out_hotel_z_24(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                return "1_STORY_OUT_HOTEL_Z_25" 
        return "1_STORY_OUT_HOTEL_Z_24" 
    
    def _1_story_out_hotel_z_25(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=3.0, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "1_STORY_OUT_HOTEL_Z_26" 
        return "1_STORY_OUT_HOTEL_Z_25" 
    
    def _1_story_out_hotel_z_26(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                return "1_STORY_OUT_HOTEL_Z_27" 

        return "1_STORY_OUT_HOTEL_Z_26" 
    
    def _1_story_out_hotel_z_27(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,95), duration=1.6, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "1_STORY_OUT_HOTEL_Z_28" 
        return "1_STORY_OUT_HOTEL_Z_27" 
    
    def _1_story_out_hotel_z_28(self):
        if self.renda_button(rendabutton="B",endpicture="3_SELECT",sub_button="A",sub_picture="TEXT_BLACK_COMMENT"):
            self.wait(0.3)
            self.etc_sendCommand("Lbutton_down")
            self.wait(0.3)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)            
            self.wait(1.0)
            return "1_STORY_OUT_HOTEL_Z_29" 
        return "1_STORY_OUT_HOTEL_Z_28" 
    
    def _1_story_out_hotel_z_29(self):
        if self.image_check("TEXT_WHITE_COMMENT2"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                return "1_STORY_OUT_HOTEL_Z_30" 

        return "1_STORY_OUT_HOTEL_Z_29" 
    
    def _1_story_out_hotel_z_30(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,140), duration=1.5, wait=1.0)
            self.press(Direction(Stick.LEFT,30), duration=2.0, wait=1.0)
            return "1_STORY_OUT_HOTEL_Z_31" 
        return "1_STORY_OUT_HOTEL_Z_30" 
    
    def _1_story_out_hotel_z_31(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                return "1_STORY_OUT_HOTEL_Z_32" 

        return "1_STORY_OUT_HOTEL_Z_31" 
    
    def _1_story_out_hotel_z_32(self):
        if self.common_skill_change_start_check() == "COMMON_SKILL_CHANGE_POKEMON_SELECT":
            return "1_STORY_OUT_HOTEL_Z_33" 

        return "1_STORY_OUT_HOTEL_Z_32" 

    def _1_story_out_hotel_z_33(self):
        if self.image_check("X_MENU_OPEN"):
            if self.image_check("SIDE_SELECT_X_MENU_W"):
                self.wait(0.5)
                for i in range(3):
                    self.etc_sendCommand("Lbutton_down")
                    self.wait(0.5)
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                for i in range(30):
                    self.pressRep(Button.B, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    if self.image_check("TEXT_WHITE_COMMENT"):
                        return "1_STORY_OUT_HOTEL_Z_34" 
            elif self.image_check("POKEMON_MENU_X_MENU_W"):
                for i in range(7):
                    self.etc_sendCommand("Lbutton_left")
                self.wait(0.5)
        return "1_STORY_OUT_HOTEL_Z_33" 
    
    def _1_story_out_hotel_z_34(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                #ネットワーク開放
                return "1_STORY_OUT_HOTEL_Z_35"  
        return "1_STORY_OUT_HOTEL_Z_34" 
    
    def _1_story_out_hotel_z_35(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,330), duration=2.5, wait=1.0)
            self.press(Direction(Stick.LEFT,100), duration=1.6, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "1_STORY_OUT_HOTEL_Z_36" 
        return "1_STORY_OUT_HOTEL_Z_35" 
    
    def _1_story_out_hotel_z_36(self):
        if self.renda_button(rendabutton="B",endpicture="3_SELECT",sub_button="A",sub_picture="TEXT_BLACK_COMMENT"):
            self.wait(0.3)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)            
            self.wait(1.0)
        return "1_STORY_OUT_HOTEL_Z_37"
    
    def _1_story_out_hotel_z_37(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=1.6, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "1_STORY_OUT_HOTEL_Z_38" 
        return "1_STORY_OUT_HOTEL_Z_37" 
    
    def _1_story_out_hotel_z_38(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                return "1_STORY_WANINOKO_SKILL_CHANGE3"
        return "1_STORY_OUT_HOTEL_Z_38"
    
    def _1_story_waninoko_skill_change3(self):
        #C+チェックできないとローリングが誤発動するパターンがあるため、AB技で戦えるようにする。
        ret = self.common_skill_change_function(2,"X","A")
        #if self.common_skill_change_current_state
        if ret == "COMMON_SKILL_CHANGE_START":
            return "1_STORY_WANINOKO_SKILL_CHANGE4"
        else: 
            return "1_STORY_WANINOKO_SKILL_CHANGE3"
        
    def _1_story_waninoko_skill_change4(self):
        #C+チェックできないとローリングが誤発動するパターンがあるため、AB技で戦えるようにする。
        ret = self.common_skill_change_function(2,"X","B")
        #if self.common_skill_change_current_state
        if ret == "COMMON_SKILL_CHANGE_START":
            return "1_STORY_WANINOKO_SKILL_CHANGE5"
        else: 
            return "1_STORY_WANINOKO_SKILL_CHANGE4"

    def _1_story_waninoko_skill_change5(self):
        #C+チェックできないとローリングが誤発動するパターンがあるため、AB技で戦えるようにする。
        ret = self.common_skill_change_function(3,"A","B")
        #if self.common_skill_change_current_state
        if ret == "COMMON_SKILL_CHANGE_START":
            return "1_STORY_WANINOKO_SKILL_CHANGE6"
        else: 
            return "1_STORY_WANINOKO_SKILL_CHANGE5"
        
    def _1_story_waninoko_skill_change6(self):
        #C+チェックできないとローリングが誤発動するパターンがあるため、AB技で戦えるようにする。
        ret = self.common_skill_change_function(3,0,"A",1)
        #if self.common_skill_change_current_state
        if ret == "COMMON_SKILL_CHANGE_START":
            return "1_STORY_WANINOKO_SKILL_CHANGE7"
        else: 
            return "1_STORY_WANINOKO_SKILL_CHANGE6" 
        
    def _1_story_waninoko_skill_change7(self):
        #C+チェックできないとローリングが誤発動するパターンがあるため、AB技で戦えるようにする。
        ret = self.common_skill_change_function(4,"X","B")
        #if self.common_skill_change_current_state
        if ret == "COMMON_SKILL_CHANGE_START":
            return "1_STORY_WANINOKO_SKILL_CHANGE8"
        else: 
            return "1_STORY_WANINOKO_SKILL_CHANGE7"  
        
    def _1_story_waninoko_skill_change8(self):
        #C+チェックできないとローリングが誤発動するパターンがあるため、AB技で戦えるようにする。
        ret = self.common_skill_change_function(5,"X","B")
        #if self.common_skill_change_current_state
        if ret == "COMMON_SKILL_CHANGE_START":
            return "1_STORY_OUT_HOTEL_Z_39_0"
        else: 
            return "1_STORY_WANINOKO_SKILL_CHANGE8"  
        
    #6体目のゲットをなくしたため破棄
    def _1_story_waninoko_skill_change9(self):
        #C+チェックできないとローリングが誤発動するパターンがあるため、AB技で戦えるようにする。
        ret = self.common_skill_change_function(6,"X","B")
        #if self.common_skill_change_current_state
        if ret == "COMMON_SKILL_CHANGE_START":
            self.wait(1.0)
            return "1_STORY_OUT_HOTEL_Z_39_0" 
        else: 
            return "1_STORY_WANINOKO_SKILL_CHANGE9"  

    def _1_story_out_hotel_z_39_0(self):
        if self.markerdir("EVENT"):
            return "1_STORY_OUT_HOTEL_Z_39" 
        else:
            return "1_STORY_OUT_HOTEL_Z_39_0"
        
    def _1_story_out_hotel_z_39(self):
        
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,99), duration=2.3, wait=0.0)
            self.press(Direction(Stick.LEFT,55), duration=5.5, wait=0.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "1_STORY_OUT_HOTEL_Z_39_1" 
        return "1_STORY_OUT_HOTEL_Z_39" 

    def _1_story_out_hotel_z_39_1(self):
        if self.markerdir("EVENT"):
            return "1_STORY_OUT_HOTEL_Z_40" 
        else:
            return "1_STORY_OUT_HOTEL_Z_39_1"
    
    def _1_story_out_hotel_z_40(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,35), duration=10.0, wait=0.0)
            self.press(Direction(Stick.LEFT,88), duration=5.2, wait=0.0)
            self.press(Direction(Stick.LEFT,45), duration=15.0, wait=0.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            for i in range(20):
                self.press(Direction(Stick.LEFT,225), duration=0.2, wait=0.3)
                self.press(Direction(Stick.LEFT,115), duration=0.35, wait=0.3)
                if self.image_check("OUT_MARKER"):
                    self.wait(0.1)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    return "1_STORY_OUT_HOTEL_Z_40_1"
        return "1_STORY_OUT_HOTEL_Z_40" 

    def _1_story_out_hotel_z_40_1(self):
        if self.markerdir("EVENT"):
            return "1_STORY_OUT_HOTEL_Z_41" 
        else:
            return "1_STORY_OUT_HOTEL_Z_40_1"
    
    def _1_story_out_hotel_z_41(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,45), duration=2.2, wait=0.0)
            return "1_STORY_OUT_HOTEL_Z_42" 
        return "1_STORY_OUT_HOTEL_Z_41" 
    
    def _1_story_out_hotel_z_42(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=0.0)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_43" 
        return "1_STORY_OUT_HOTEL_Z_42" 
    
    def _1_story_out_hotel_z_43(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            if self.image_check("FIELD3") or self.image_check("FIELD_BACK3"):
                self.wait(1.0)
                self.etc_sendCommand("Lbutton_up")
                self.wait(1.0)
                return "1_STORY_OUT_HOTEL_Z_44" 
            else:
                self.etc_sendCommand("Lbutton_left")
                self.wait(0.3)
        return "1_STORY_OUT_HOTEL_Z_43"
    
    def _1_story_out_hotel_z_44(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            for i in range(3):
                self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=0)
            return "1_STORY_OUT_HOTEL_Z_45" 
        return "1_STORY_OUT_HOTEL_Z_44" 
    
    def _1_story_out_hotel_z_45(self):
        if self.image_check("IN_MARKER"):
            self.wait(0.1)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_47" 
        elif self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,300), duration=0.5, wait=0.5)
            self.press(Direction(Stick.LEFT,90), duration=6.5, wait=0.5)
            return "1_STORY_OUT_HOTEL_Z_46" 
        return "1_STORY_OUT_HOTEL_Z_45" 
    
    def _1_story_out_hotel_z_46(self):
        if self.image_check("IN_MARKER"):
            self.wait(0.1)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_47" 
        elif self.markerdir("EVENT"):
            #いわくだきできていない用に
            return "1_STORY_OUT_HOTEL_Z_44" 
        else:
            return "1_STORY_OUT_HOTEL_Z_46"
    
    def _1_story_out_hotel_z_47(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="WANINOKO_ICON",sub_button="A",sub_picture="1_SELECT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                return "1_STORY_OUT_HOTEL_Z_48"  
        return "1_STORY_OUT_HOTEL_Z_47" 
    
    def _1_story_out_hotel_z_48(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,102), duration=1.2, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_49" 
        return "1_STORY_OUT_HOTEL_Z_48" 
    
    def _1_story_out_hotel_z_49(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.5, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_50" 
        return "1_STORY_OUT_HOTEL_Z_49" 
    
    def _1_story_out_hotel_z_50(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="WANINOKO_ICON",sub_button="A",sub_picture="1_SELECT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                return "1_STORY_OUT_HOTEL_Z_51"  
        return "1_STORY_OUT_HOTEL_Z_50"
    
    def _1_story_out_hotel_z_51(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=6.0, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_52" 
        return "1_STORY_OUT_HOTEL_Z_51"
    
    def _1_story_out_hotel_z_52(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="WANINOKO_ICON",sub_button="A",sub_picture="1_SELECT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                return "1_STORY_OUT_HOTEL_Z_53"  

        return "1_STORY_OUT_HOTEL_Z_52"
    
    
    def _1_story_out_hotel_z_53(self):
        ### AUTO_SAVE_POINT
        ret = self.Common_map_open()
        if  ret == "COMMON_GOTO_SELECT1":
            return "1_STORY_OUT_HOTEL_Z_54"
        return "1_STORY_OUT_HOTEL_Z_53"
    
    def _1_story_out_hotel_z_54(self):
        #イベントマーカーがないため、方向を確定させられるようにマーカーを設置する。
        if self.image_check("MAP2"):  
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(0.5)
            self.pressRep(Button.B, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_55"
        return "1_STORY_OUT_HOTEL_Z_54"
    
    def _1_story_out_hotel_z_55(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=4.75, wait=0.5)
            self.press(Direction(Stick.LEFT,180), duration=0.1, wait=0.5)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_56"
        return "1_STORY_OUT_HOTEL_Z_55"
    
    def _1_story_out_hotel_z_56(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=4.75, wait=0.5)
            return "1_STORY_OUT_HOTEL_Z_57"
        return "1_STORY_OUT_HOTEL_Z_56"
    
    def _1_story_out_hotel_z_57(self):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE"):
            self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_GREEN_COMMENT"):
            return "1_STORY_OUT_HOTEL_Z_58"
        return "1_STORY_OUT_HOTEL_Z_57"
    
    def _1_story_out_hotel_z_58(self):
        if self.image_check("TEXT_GREEN_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="1_SELECT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                return "1_STORY_OUT_HOTEL_Z_59"  
        return "1_STORY_OUT_HOTEL_Z_58"
    
    # 敗北用フォローを入れるか、リロード対応を入れた方がよい。位置が変わるのでリロードが良い
    def _1_story_out_hotel_z_59(self):
        ### AUTO_SAVE_POINT
        if self.markerdir("PIN"):
            return "1_STORY_OUT_HOTEL_Z_60" 
        else:
            return "1_STORY_OUT_HOTEL_Z_59"

    def _1_story_out_hotel_z_60(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,330), duration=4.0, wait=0.5)
            return "1_STORY_OUT_HOTEL_Z_60_1"
        return "1_STORY_OUT_HOTEL_Z_60" 
    
    def _1_story_out_hotel_z_60_1(self):
        if self.markerdir("PIN"):
            return "1_STORY_OUT_HOTEL_Z_60_2" 
        else:
            return "1_STORY_OUT_HOTEL_Z_60_1"
    
    def _1_story_out_hotel_z_60_2(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,180), duration=9.0, wait=0.5)
            self.press(Direction(Stick.LEFT,240), duration=9.0, wait=0.5)
            return "1_STORY_OUT_HOTEL_Z_61"
        return "1_STORY_OUT_HOTEL_Z_60_2" 
    
    def _1_story_out_hotel_z_61(self):
        if self.markerdir("PIN"):
            return "1_STORY_OUT_HOTEL_Z_62" 
        else:
            return "1_STORY_OUT_HOTEL_Z_61"
    
    def _1_story_out_hotel_z_62(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,120), duration=1.4, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_63" 
        return "1_STORY_OUT_HOTEL_Z_62" 
    
    def _1_story_out_hotel_z_63(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                return "1_STORY_OUT_HOTEL_Z_64" 
        return "1_STORY_OUT_HOTEL_Z_63" 
    
    def _1_story_out_hotel_z_64(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,87), duration=4.0, wait=0.5)
            self.etc_sendCommand("Lbutton_up")
            self.press(Direction(Stick.LEFT,90), duration=0.5, wait=0.5)
            return "1_STORY_OUT_HOTEL_Z_65" 
        return "1_STORY_OUT_HOTEL_Z_64" 
    
    def _1_story_out_hotel_z_65(self):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE"):
            self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_GREEN_COMMENT"):
            return "1_STORY_OUT_HOTEL_Z_66"
        elif self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1)
        return "1_STORY_OUT_HOTEL_Z_65" 
    
    def _1_story_out_hotel_z_66(self):
        if self.image_check("TEXT_GREEN_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="1_SELECT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                return "1_STORY_OUT_HOTEL_Z_67"  

        return "1_STORY_OUT_HOTEL_Z_66" 
    
    def _1_story_out_hotel_z_67(self):
        ### AUTO_SAVE_POINT
        if self.markerdir("PIN"):
            self.wait(0.5)
            self.etc_sendCommand("Lbutton_down")
            return "1_STORY_OUT_HOTEL_Z_68" 
        else:
            return "1_STORY_OUT_HOTEL_Z_67"
    
    def _1_story_out_hotel_z_68(self):
        #回復ように移動
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,30), duration=4.0, wait=0.5)
            self.press(Direction(Stick.LEFT,300), duration=5.0, wait=0.5)
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=0.5)
            self.press(Direction(Stick.LEFT,300), duration=6.0, wait=0.5)
            self.press(Direction(Stick.LEFT,120), duration=20.0, wait=0.5)
            self.press(Direction(Stick.LEFT,270), duration=3.2, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_69" 

        return "1_STORY_OUT_HOTEL_Z_68" 
    
    def _1_story_out_hotel_z_69(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="1_SELECT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
            return "1_STORY_OUT_HOTEL_Z_70"
        return "1_STORY_OUT_HOTEL_Z_69" 
    
    def _1_story_out_hotel_z_70(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,0), duration=5.0, wait=0.5)
            self.press(Direction(Stick.LEFT,70), duration=0.5, wait=0.5)
            self.press(Direction(Stick.LEFT,30), duration=5.0, wait=0.5)
            self.press(Direction(Stick.LEFT,330), duration=5.0, wait=0.5)
            self.press(Direction(Stick.LEFT,30), duration=5.0, wait=0.5)
            self.press(Direction(Stick.LEFT,250), duration=10.0, wait=0.5)
            self.press(Direction(Stick.LEFT,300), duration=5.0, wait=0.5)
            self.press(Direction(Stick.LEFT,220), duration=3.0, wait=0.5)
            return "1_STORY_OUT_HOTEL_Z_71" 

        return "1_STORY_OUT_HOTEL_Z_70"
    
    def _1_story_out_hotel_z_71(self):
        if self.markerdir("PIN"):
            return "1_STORY_OUT_HOTEL_Z_72" 
        else:
            return "1_STORY_OUT_HOTEL_Z_71"
    
    def _1_story_out_hotel_z_72(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,355), duration=15.0, wait=0.5)
            self.press(Direction(Stick.LEFT,200), duration=1.2, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_73" 
        return "1_STORY_OUT_HOTEL_Z_72"
    
    def _1_story_out_hotel_z_73(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
            return "1_STORY_OUT_HOTEL_Z_74"
        return "1_STORY_OUT_HOTEL_Z_73"
    
    def _1_story_out_hotel_z_74(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,45), duration=5.0, wait=0.5)
            self.press(Direction(Stick.LEFT,320), duration=1.2, wait=0.5)
            self.press(Direction(Stick.LEFT,290), duration=2.0, wait=0.5)
            self.press(Direction(Stick.LEFT,30), duration=1.2, wait=0.5)
            self.press(Direction(Stick.LEFT,320), duration=1.2, wait=0.5)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_75" 
        return "1_STORY_OUT_HOTEL_Z_74"
    
    def _1_story_out_hotel_z_75(self):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE"):
            self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_GREEN_COMMENT"):
            return "1_STORY_OUT_HOTEL_Z_76"
        elif self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1)

        return "1_STORY_OUT_HOTEL_Z_75"
    
    def _1_story_out_hotel_z_76(self):
        if self.image_check("TEXT_GREEN_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                return "1_STORY_OUT_HOTEL_Z_77"  

        return "1_STORY_OUT_HOTEL_Z_76"
    
    def _1_story_out_hotel_z_77(self):
        ret = self.Common_goto(2,0,0)#ポケセンベールで回復
        
        if ret == "START":
            return "1_STORY_OUT_HOTEL_Z_78"
        else:
            return "1_STORY_OUT_HOTEL_Z_77"
    
    def _1_story_out_hotel_z_78(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT, 90), duration=2.3, wait=0.1)
            self.wait(0.1)
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            self.wait(0.1)
            self.pressRep(Button.B, repeat=50, duration=0.15, wait=0.5, interval=0.1)
            self.wait(0.1)
            return "1_STORY_OUT_HOTEL_Z_79"
        return "1_STORY_OUT_HOTEL_Z_78"
    
    def _1_story_out_hotel_z_79(self):
        ret = self.Common_goto(2,0,0)#ポケセンベールに移動で位置確定
        
        if ret == "START":
            return "1_STORY_OUT_HOTEL_Z_80"
        else:
            return "1_STORY_OUT_HOTEL_Z_79"
    
    def _1_story_out_hotel_z_80(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,355), duration=1.3, wait=0.5)
            self.press(Direction(Stick.LEFT,92), duration=2.2, wait=0.5)
            self.press(Direction(Stick.LEFT,180), duration=0.1, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_81"
        return "1_STORY_OUT_HOTEL_Z_80"
    
    def _1_story_out_hotel_z_81(self):
        self.wait(3.0)
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                return "1_STORY_OUT_HOTEL_Z_82" 
        elif self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            return "1_STORY_OUT_HOTEL_Z_79"
        return "1_STORY_OUT_HOTEL_Z_81"
    
    def _1_story_out_hotel_z_82(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=20.0, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_83"
        return "1_STORY_OUT_HOTEL_Z_82"
    
    def _1_story_out_hotel_z_83(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="BATTLE_BALL_CHECK",endpicture2="ESCAPE",sub_button="A",sub_picture="3_SELECT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                return "1_STORY_OUT_HOTEL_Z_84" 
        return "1_STORY_OUT_HOTEL_Z_83"
    
    #Zランク
    def _1_story_out_hotel_z_84(self):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE") or self.image_check("TEXT_WHITE_COMMENT"):
            self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_83"
        elif self.image_check("COIN_ICON"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "1_STORY_OUT_HOTEL_Z_85"
        return "1_STORY_OUT_HOTEL_Z_84"
    
    def _1_story_out_hotel_z_85(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="IN_ICON",sub_button="A",sub_picture="3_SELECT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER",sub4_button="A",sub4_picture="MORNING"):
                self.wait(1.0)
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                return "1_STORY_END"
        return "1_STORY_OUT_HOTEL_Z_85"
    
    def _1_story_end(self):
        return "1_STORY_START_CHECK" 

    ######################################################
    # MAIN_2_Y_V_LANK SUB FUNCTION
    ######################################################
    def _2_story_start_check(self):
        ### AUTO_SAVE_POINT
        if self.image_check("IN_ICON"):
            return "2_STORY_TOWER_1"
        else:
            return "2_STORY_START_CHECK"
    
    def _2_story_tower_1(self):
        if self.image_check("IN_ICON"):
            self.press(Direction(Stick.LEFT,100), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_TOWER_2"
        return "2_STORY_TOWER_1"
    
    def _2_story_tower_2(self):
        if self.markerdir("EVENT",nofiled=True):
            return "2_STORY_TOWER_3"
        else:
            return "2_STORY_TOWER_2"
    
    def _2_story_tower_3(self):
        if self.image_check("EVENT_MARKER_CENTER"):
            self.press(Direction(Stick.LEFT,90), duration=2.4, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_TOWER_4"
        return "2_STORY_TOWER_3"
    
    def _2_story_tower_4(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            return "2_STORY_TOWER_5"
        return "2_STORY_TOWER_4"
    
    def _2_story_tower_5(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_TOWER_6"
        return "2_STORY_TOWER_5"
    
    def _2_story_tower_6(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            return "2_STORY_TOWER_7"
        return "2_STORY_TOWER_6"
    
    def _2_story_tower_7(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=4.0, wait=1.0)
            self.wait(0.5)
            return "2_STORY_TOWER_8"
        else:
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_TOWER_7"
        return "2_STORY_TOWER_7"
    
    def _2_story_tower_8(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_TOWER_9"
        return "2_STORY_TOWER_8"
    
    def _2_story_tower_9(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            if self.image_check("FIELD_W"):
                self.etc_sendCommand("Lbutton_up")
            self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            return "2_STORY_TOWER_10"
        return "2_STORY_TOWER_9"
    
    def _2_story_tower_10(self):
        if self.image_check("TEXT_BLACK_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_TOWER_11"
        return "2_STORY_TOWER_10"
    
    def _2_story_tower_11(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,100), duration=0.7, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.press(Direction(Stick.LEFT,90), duration=15.0, wait=0.5)
            self.press(Direction(Stick.LEFT,150), duration=0.3, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=10.0, wait=0.5)
            return "2_STORY_TOWER_12"
        return "2_STORY_TOWER_11"
    
    def _2_story_tower_12(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_TOWER_13"
        return "2_STORY_TOWER_12"
    
    def _2_story_tower_13(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=14.0, wait=0.5)
            self.press(Direction(Stick.LEFT,270), duration=1.5, wait=0.5)
            self.press(Direction(Stick.LEFT,0), duration=3.0, wait=0.5)
            return "2_STORY_TOWER_14"
        return "2_STORY_TOWER_13"
    
    def _2_story_tower_14(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_TOWER_15_0"
        return "2_STORY_TOWER_14"
    
    def _2_story_tower_15_0(self):
        ### AUTO_SAVE_POINT
        if self.markerdir("EVENT",nofiled=True):
            return "2_STORY_TOWER_15"
        else:
            return "2_STORY_TOWER_15_0"
    def _2_story_tower_15(self):
        
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,85), duration=12.0, wait=0.5)
            return "2_STORY_TOWER_16"
        return "2_STORY_TOWER_15"
    
    def _2_story_tower_16(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_TOWER_17"
        return "2_STORY_TOWER_16"
    
    def _2_story_tower_17(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=0.5)
            return "2_STORY_TOWER_18"
        return "2_STORY_TOWER_17"
    
    def _2_story_tower_18(self):
        if self.image_check("TEXT_GREEN_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_TOWER_19"
        return "2_STORY_TOWER_18"
    
    def _2_story_tower_19(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,140), duration=9.0, wait=0.5)
            self.press(Direction(Stick.LEFT,90), duration=11.5, wait=0.5)
            self.press(Direction(Stick.LEFT,50), duration=10.0, wait=0.5)
            self.press(Direction(Stick.LEFT,95), duration=14.0, wait=0.5)
            return "2_STORY_TOWER_20"
        return "2_STORY_TOWER_19"
    
    def _2_story_tower_20(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="4_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_TOWER_21"
        return "2_STORY_TOWER_20"
    
    def _2_story_tower_21(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=10.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,105), duration=11.5, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,160), duration=14.0, wait=0.5)
            return "2_STORY_TOWER_22"
        return "2_STORY_TOWER_21"
    
    def _2_story_tower_22(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="4_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_TOWER_23"
        return "2_STORY_TOWER_22"
    
    def _2_story_tower_23(self):
        #ポケモンセンターのスポット登録
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,12), duration=10.0, wait=0.5)
            return "2_STORY_TOWER_24"
        return "2_STORY_TOWER_23"
    
    def _2_story_tower_24(self):
        ret = self.Common_goto(2,0,1)#ポケセンメディオに移動で位置確定
        
        if ret == "START":
            return "2_STORY_TOWER_25"
        else:
            return "2_STORY_TOWER_24"
    
    def _2_story_tower_25(self):
        ### AUTO_SAVE_POINT
        if self.markerdir("EVENT"):
            return "2_STORY_TOWER_26"
        else:
            return "2_STORY_TOWER_25"
    
    def _2_story_tower_26(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=14.0, wait=0.5)
            return "2_STORY_TOWER_27"
        return "2_STORY_TOWER_26"
    
    def _2_story_tower_27(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="BATTLE_BALL_CHECK",endpicture2="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="4_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_TOWER_28"
        return "2_STORY_TOWER_27"
    
    def _2_story_tower_28(self):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE") or self.image_check("TEXT_WHITE_COMMENT"):
            self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("2_SELECT"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_TOWER_28"
        elif self.image_check("COIN_ICON"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_TOWER_29"
        return "2_STORY_TOWER_28"
    
    def _2_story_tower_29(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="4_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_TOWER_30"
        return "2_STORY_TOWER_29"
    
    def _2_story_tower_30(self):
        ret = self.Common_goto(2,0,1)#ポケセンメディオに移動で位置確定
        if ret == "START":
            return "2_STORY_TOWER_31"
        else:
            return "2_STORY_TOWER_30"
    
    def _2_story_tower_31(self):
        ### AUTO_SAVE_POINT
        if self.Common_pokemon_recovery():
            return "2_STORY_TOWER_32"
        else:
            return "2_STORY_TOWER_31"
    
    def _2_story_tower_32(self):
        ret = self.Common_goto(2,0,1)#ポケセンメディオに移動で位置確定
        if ret == "START":
            return "2_STORY_TOWER_33"
        else:
            return "2_STORY_TOWER_32"
    
    def _2_story_tower_33(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,186), duration=20.0, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_TOWER_34"
        return "2_STORY_TOWER_33"
    
    def _2_story_tower_34(self):
        if self.markerdir("EVENT"):
            return "2_STORY_TOWER_35"
        else:
            return "2_STORY_TOWER_34"
    
    def _2_story_tower_35(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,55), duration=5.5, wait=0.5)
            self.press(Direction(Stick.LEFT,33), duration=1.0, wait=0.5)
            self.press(Direction(Stick.LEFT,240), duration=12.0, wait=0.5)
            self.press(Direction(Stick.LEFT,55), duration=0.8, wait=0.5)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_TOWER_36"
        
        return "2_STORY_TOWER_35"
    
    def _2_story_tower_36(self):
        if self.image_check("PIKA_ICON_GET6"):
            if self.image_check("EYE_CHECK"):
                if self.image_check("FIELD_W"):
                    self.etc_sendCommand("Lbutton_up")
                self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1,lockon_endskip=1)
            else:
                self.ZL_ACTION("END")
                return "2_STORY_TOWER_37"
        if self.image_check("GETCHANCE_ICON4"):
            self.get_pokemon()
            self.wait(2.0)
            #ゲット時に自動でセーブされてしまうため大体の位置を確定させたいため待機
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            if self.image_check("FIELD_W"):
                self.etc_sendCommand("Lbutton_up")
            self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1,lockon_endskip=1)

        return "2_STORY_TOWER_36"
    
    def _2_story_tower_37(self):
        ret = self.Common_goto(2,0,1)#ポケセンメディオに移動で位置確定
        if ret == "START":
            return "2_STORY_TOWER_38"
        else:
            return "2_STORY_TOWER_37"
    
    def _2_story_tower_38(self):
        ### AUTO_SAVE_POINT
        if self.Common_pokemon_recovery():
            return "2_STORY_TOWER_39"
        else:
            return "2_STORY_TOWER_38"
    
    def _2_story_tower_39(self):
        ret = self.Common_goto(2,0,1)#ポケセンメディオに移動で位置確定
        if ret == "START":
            return "2_STORY_TOWER_40"
        else:
            return "2_STORY_TOWER_39"
    
    def _2_story_tower_40(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,185), duration=15.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,170), duration=10.0, wait=0.5)
            self.press(Direction(Stick.LEFT,110), duration=11.0, wait=0.5)
            self.press(Direction(Stick.LEFT,55), duration=10.0, wait=0.5)
            self.press(Direction(Stick.LEFT,120), duration=8.0, wait=0.5)
            return "2_STORY_TOWER_41"

        return "2_STORY_TOWER_40"
    
    def _2_story_tower_41(self):
        if self.story_Template_Comment_Out():
            return "2_STORY_TOWER_42"
        return "2_STORY_TOWER_41"
    
    def _2_story_tower_42(self):
        ### AUTO_SAVE_POINT?
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=0.8, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_TOWER_43"
        return "2_STORY_TOWER_42"
    
    def _2_story_tower_43(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            #誤検知するため・上下アイコンが表示されないためワニノコ・メリープアイコンで判定
            #if self.renda_button(rendabutton="B",endpicture="WANINOKO_ICON",endpicture2="MERIP_ICON_GET5",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="4_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            if self.renda_button(rendabutton="B",endpicture="EVENT_MARKER_CENTER_WIDE",endpicture2="EVENT_MARKER_RIGHT_WIDE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="4_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_TOWER_44"
        return "2_STORY_TOWER_43"
    
    def _2_story_tower_44(self):
        ### AUTO_SAVE_POINT
        #if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
        if self.image_check("EVENT_MARKER_CENTER_WIDE") or self.image_check("EVENT_MARKER_RIGHT_WIDE"):
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_TOWER_45"
        return "2_STORY_TOWER_44"
    
    def _2_story_tower_45(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="EVENT_MARKER_CENTER_WIDE",endpicture2="EVENT_MARKER_RIGHT_WIDE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="4_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_TOWER_46"
        return "2_STORY_TOWER_45"
    
    def _2_story_tower_46(self):
        if self.image_check("EVENT_MARKER_CENTER_WIDE") or self.image_check("EVENT_MARKER_RIGHT_WIDE"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,230), duration=1.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_1"
        return "2_STORY_TOWER_46"

    def _2_story_mapping_1(self):
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(1,0,-1)#ハンサムハウスに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_2"
        else:
            return "2_STORY_MAPPING_1"
    
    def _2_story_mapping_2(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=8.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,250), duration=6.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,170), duration=16.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,80), duration=5.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_3"
        return "2_STORY_MAPPING_2"
    
    def _2_story_mapping_3(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_W_ZONE4"):
                print("MOVEPOINT_TARGET_W_ZONE4")
            if self.image_check("MOVEPOINT_PIC_W_ZONE4"):
                print("MOVEPOINT_PIC_W_ZONE4")
            
        else:
            ret = self.Common_goto(4,0,-1,movepoint_check=1)#ゾーン4が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_W_ZONE4",pic2="MOVEPOINT_PIC_W_ZONE4") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_5"#再移動となるため5にジャンプ
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_1"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_3"
            else:
                return "2_STORY_MAPPING_3"
        return "2_STORY_MAPPING_3"
    
    def _2_story_mapping_4(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(4,0,-1)#ゾーン4
        if ret == "START":
            return "2_STORY_MAPPING_5"
        else:
            return "2_STORY_MAPPING_4"
    
    def _2_story_mapping_5(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=15.5, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=4.0, wait=0.5)
            self.wait(1.0)
            return "2_STORY_MAPPING_6"
        return "2_STORY_MAPPING_5"
    
    def _2_story_mapping_6(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_POKECENTER_RUDU"):
                print("MOVEPOINT_TARGET_POKECENTER_RUDU")
            if self.image_check("MOVEPOINT_PIC_POKECENTER_RUDU"):
                print("MOVEPOINT_PIC_POKECENTER_RUDU")
            
        else:
            ret = self.Common_goto(2,0,1,movepoint_check=1)#ポケセンルージュが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_POKECENTER_RUDU",pic2="MOVEPOINT_PIC_POKECENTER_RUDU") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_7"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_4"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_6"
            else:
                return "2_STORY_MAPPING_6"
        return "2_STORY_MAPPING_6"
    
    def _2_story_mapping_7(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(4,0,-1)#ゾーン4
        if ret == "START":
            return "2_STORY_MAPPING_8"
        else:
            return "2_STORY_MAPPING_7"
    
    def _2_story_mapping_8(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,0), duration=10.5, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_9"
        return "2_STORY_MAPPING_8"
    
    def _2_story_mapping_9(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_RESTAURANT_DREAM"):
                print("MOVEPOINT_TARGET_RESTAURANT_DREAM")
            if self.image_check("MOVEPOINT_PIC_RESTAURANT_DREAM"):
                print("MOVEPOINT_PIC_RESTAURANT_DREAM")
            
        else:
            ret = self.Common_goto(1,0,-1,movepoint_check=1)#ポケセンルージュが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_RESTAURANT_DREAM",pic2="MOVEPOINT_PIC_RESTAURANT_DREAM") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_10"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_7"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_9"
            else:
                return "2_STORY_MAPPING_9"
        return "2_STORY_MAPPING_9"
    
    def _2_story_mapping_10(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(1,0,0)#プリズムタワー
        if ret == "START":
            return "2_STORY_MAPPING_11"
        else:
            return "2_STORY_MAPPING_10"
    
    def _2_story_mapping_11(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,140), duration=18.5, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,195), duration=18.5, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,105), duration=2.0, wait=0.5) 
            return "2_STORY_MAPPING_12"
        return "2_STORY_MAPPING_11"
    
    def _2_story_mapping_12(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_CAFE_MAN"):
                print("MOVEPOINT_TARGET_CAFE_MAN")
            if self.image_check("MOVEPOINT_PIC_CAFE_MAN"):
                print("MOVEPOINT_PIC_CAFE_MAN")
            
        else:
            ret = self.Common_goto(3,0,-1,movepoint_check=1)#カフェ・おとこまえが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_CAFE_MAN",pic2="MOVEPOINT_PIC_CAFE_MAN") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_14"#再移動となるため14にジャンプ
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_10"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_12"
            else:
                return "2_STORY_MAPPING_12"
        return "2_STORY_MAPPING_12"
    
    def _2_story_mapping_13(self):
        ### AUTO_SAVE_POINT
        ret = self.Common_goto(3,0,-1)#カフェ・おとこまえ
        if ret == "START":
            return "2_STORY_MAPPING_14"
        else:
            return "2_STORY_MAPPING_13"
    
    def _2_story_mapping_14(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=4.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=20.0, wait=0.5)
            self.wait(1.0)
            #self.press(Direction(Stick.LEFT,105), duration=2.0, wait=0.5) 
            return "2_STORY_MAPPING_15"
        return "2_STORY_MAPPING_14"
    
    def _2_story_mapping_15(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_ROSE_SQUARE"):
                print("MOVEPOINT_TARGET_ROSE_SQUARE")
            if self.image_check("MOVEPOINT_PIC_ROSE_SQUARE"):
                print("MOVEPOINT_PIC_ROSE_SQUARE")
            
        else:
            ret = self.Common_goto(1,0,4,movepoint_check=1)#ローズ広場が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_ROSE_SQUARE",pic2="MOVEPOINT_PIC_ROSE_SQUARE") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_17"#再移動となるため17にジャンプ
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_13"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_15"
            else:
                return "2_STORY_MAPPING_15"
        return "2_STORY_MAPPING_15"
    
    def _2_story_mapping_16(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(1,0,4)#ローズ広場
        if ret == "START":
            return "2_STORY_MAPPING_17"
        else:
            return "2_STORY_MAPPING_16"
    
    def _2_story_mapping_17(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=5.5, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,270), duration=2.0, wait=0.5) 
            self.wait(1.0)
            return "2_STORY_MAPPING_18"
        return "2_STORY_MAPPING_17"
    
    def _2_story_mapping_18(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_POKECENTER_ROSE_S"):
                print("MOVEPOINT_TARGET_POKECENTER_ROSE_S")
            if self.image_check("MOVEPOINT_PIC_POKECENTER_ROSE_S"):
                print("MOVEPOINT_PIC_POKECENTER_ROSE_S")
            
        else:
            ret = self.Common_goto(2,0,1,movepoint_check=1)#ポケセンローズ広場が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_POKECENTER_ROSE_S",pic2="MOVEPOINT_PIC_POKECENTER_ROSE_S") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_19"#再移動となるため17にジャンプ
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_16"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_18"
            else:
                return "2_STORY_MAPPING_18"
        return "2_STORY_MAPPING_18"
    
    def _2_story_mapping_19(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(1,0,4)#ローズ広場
        if ret == "START":
            return "2_STORY_MAPPING_20"
        else:
            return "2_STORY_MAPPING_19"
    
    def _2_story_mapping_20(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,75), duration=20.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=32.0, wait=0.5) 
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,0), duration=4.0, wait=0.5) 
            self.wait(1.0)
            return "2_STORY_MAPPING_21"
        return "2_STORY_MAPPING_20"
    
    def _2_story_mapping_21(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_POKECENTER_ROSE"):
                print("MOVEPOINT_TARGET_POKECENTER_ROSE")
            if self.image_check("MOVEPOINT_PIC_POKECENTER_ROSE"):
                print("MOVEPOINT_PIC_POKECENTER_ROSE")
            
        else:
            ret = self.Common_goto(2,0,1,movepoint_check=1)#ポケセンローズが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_POKECENTER_ROSE",pic2="MOVEPOINT_PIC_POKECENTER_ROSE") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_22"#再移動となるため17にジャンプ
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_19"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_21"
            else:
                return "2_STORY_MAPPING_21"
        return "2_STORY_MAPPING_21"
    
    def _2_story_mapping_22(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(1,0,0)#プリズムタワーに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_23"
        else:
            return "2_STORY_MAPPING_22"
    
    def _2_story_mapping_23(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,270), duration=39.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=6.0, wait=0.5) 
            self.wait(1.0)
            #self.press(Direction(Stick.LEFT,0), duration=4.0, wait=0.5) 
            #self.wait(1.0)
            return "2_STORY_MAPPING_24"
        return "2_STORY_MAPPING_23"
    
    def _2_story_mapping_24(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_POKECENTER_PRANTAN"):
                print("MOVEPOINT_TARGET_POKECENTER_PRANTAN")
            if self.image_check("MOVEPOINT_PIC_POKECENTER_PRANTAN"):
                print("MOVEPOINT_PIC_POKECENTER_PRANTAN")
            
        else:
            ret = self.Common_goto(2,0,1,movepoint_check=1)#ポケセンプランタンが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_POKECENTER_PRANTAN",pic2="MOVEPOINT_PIC_POKECENTER_PRANTAN") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_25"#再移動となるため17にジャンプ
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_22"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_24"
            else:
                return "2_STORY_MAPPING_24"
        return "2_STORY_MAPPING_24"
    
    def _2_story_mapping_25(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(1,0,2)#ポケモン研究所に移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_26"
        else:
            return "2_STORY_MAPPING_25"
    
    def _2_story_mapping_26(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,0), duration=0.1, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=6.0, wait=0.5) 
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,75), duration=0.1, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=20.0, wait=0.5) 
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,85), duration=0.1, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=32.0, wait=0.5) 
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,5), duration=0.1, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=10.0, wait=0.5) 
            self.wait(1.0)
            #self.press(Direction(Stick.LEFT,0), duration=4.0, wait=0.5) 
            #self.wait(1.0)
            return "2_STORY_MAPPING_27"
        return "2_STORY_MAPPING_26"
    
    def _2_story_mapping_27(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_POKECENTER_BLUE"):
                print("MOVEPOINT_TARGET_POKECENTER_BLUE")
            if self.image_check("MOVEPOINT_PIC_POKECENTER_BLUE"):
                print("MOVEPOINT_PIC_POKECENTER_BLUE")
            
        else:
            ret = self.Common_goto(2,0,1,movepoint_check=1)#ポケセンプランタンが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_POKECENTER_BLUE",pic2="MOVEPOINT_PIC_POKECENTER_BLUE") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_28"#再移動となるため17にジャンプ
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_25"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_27"
            else:
                return "2_STORY_MAPPING_27"
        return "2_STORY_MAPPING_27"
    
    def _2_story_mapping_28(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(4,0,1)#ワイルドゾーン3に移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_29"
        else:
            return "2_STORY_MAPPING_28"
    
    def _2_story_mapping_29(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,30), duration=10.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,320), duration=16.2, wait=0.5) 
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,50), duration=20.6, wait=0.5) 
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,320), duration=7.0, wait=0.5) 
            self.wait(1.0)
            return "2_STORY_MAPPING_30"
        return "2_STORY_MAPPING_29"
    
    def _2_story_mapping_30(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_POKECENTER_EVEL"):
                print("MOVEPOINT_TARGET_POKECENTER_EVEL")
            if self.image_check("MOVEPOINT_PIC_POKECENTER_EVEL"):
                print("MOVEPOINT_PIC_POKECENTER_EVEL")
            
        else:
            ret = self.Common_goto(2,0,-1,movepoint_check=1)#ポケセンイベールが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_POKECENTER_EVEL",pic2="MOVEPOINT_PIC_POKECENTER_EVEL") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_32"#再移動となるため32にジャンプ
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_28"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_30"
            else:
                return "2_STORY_MAPPING_30"
        return "2_STORY_MAPPING_30"
    
    def _2_story_mapping_31(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(2,0,-1)#ポケセンイベールに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_32"
        else:
            return "2_STORY_MAPPING_31"
    
    def _2_story_mapping_32(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,350), duration=4.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,270), duration=30.0, wait=0.5) 
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,190), duration=10.0, wait=0.5) 
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,160), duration=15.0, wait=0.5) 
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,170), duration=7.0, wait=0.5) 
            self.wait(1.0)
            return "2_STORY_MAPPING_33"
        return "2_STORY_MAPPING_32"
    
    def _2_story_mapping_33(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_CAFE_RETAKE"):
                print("MOVEPOINT_TARGET_CAFE_RETAKE")
            if self.image_check("MOVEPOINT_PIC_CAFE_RETAKE"):
                print("MOVEPOINT_PIC_CAFE_RETAKE")
            
        else:
            ret = self.Common_goto(3,0,-1,movepoint_check=1)#カフェリテイクが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_CAFE_RETAKE",pic2="MOVEPOINT_PIC_CAFE_RETAKE") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_35"#再移動となるため35にジャンプ
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_31"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_33"
            else:
                return "2_STORY_MAPPING_33"
        return "2_STORY_MAPPING_33"
    
    def _2_story_mapping_34(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(3,0,-1)##カフェリテイクに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_35"
        else:
            return "2_STORY_MAPPING_34"
    
    def _2_story_mapping_35(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=15.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,140), duration=4.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,80), duration=4.0, wait=0.5)
            self.wait(1.0)
            return "2_STORY_MAPPING_36"
        return "2_STORY_MAPPING_35"
    
    def _2_story_mapping_36(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_POKECENTER_JONE"):
                print("MOVEPOINT_TARGET_POKECENTER_JONE")
            if self.image_check("MOVEPOINT_PIC_POKECENTER_JONE"):
                print("MOVEPOINT_PIC_POKECENTER_JONE")
            
        else:
            ret = self.Common_goto(2,0,-2,movepoint_check=1)#ポケセンジョーヌが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_POKECENTER_JONE",pic2="MOVEPOINT_PIC_POKECENTER_JONE") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_37"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_34"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_36"
            else:
                return "2_STORY_MAPPING_36"
        return "2_STORY_MAPPING_36"
    
    def _2_story_mapping_37(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(3,0,1)##ヌーヴォカフェに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_38"
        else:
            return "2_STORY_MAPPING_37"
    
    def _2_story_mapping_38(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=15.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_39"
        return "2_STORY_MAPPING_38"
    
    def _2_story_mapping_39(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_W_ZONE2"):
                print("MOVEPOINT_TARGET_W_ZONE2")
            if self.image_check("MOVEPOINT_PIC_W_ZONE2"):
                print("MOVEPOINT_PIC_W_ZONE2")
            
        else:
            ret = self.Common_goto(4,0,1,movepoint_check=1)#ワイルドゾーン2が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_W_ZONE2",pic2="MOVEPOINT_PIC_W_ZONE2") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_40"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_37"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_39"
            else:
                return "2_STORY_MAPPING_39"
        return "2_STORY_MAPPING_39"
    
    def _2_story_mapping_40(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(1,0,0)#プリズムタワーに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_41"
        else:
            return "2_STORY_MAPPING_40"

    
    def _2_story_mapping_41(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,170), duration=11.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_42"
        return "2_STORY_MAPPING_41"

    def _2_story_mapping_42(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_W_ZONE5"):
                print("MOVEPOINT_TARGET_W_ZONE5")
            if self.image_check("MOVEPOINT_PIC_W_ZONE5"):
                print("MOVEPOINT_PIC_W_ZONE5")
            
        else:
            ret = self.Common_goto(4,0,-1,movepoint_check=1)#ワイルドゾーン5が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_W_ZONE5",pic2="MOVEPOINT_PIC_W_ZONE5") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_43"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_40"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_42"
            else:
                return "2_STORY_MAPPING_42"
        return "2_STORY_MAPPING_42"
    
    def _2_story_mapping_43(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(2,0,-2)#ポケセンタージョーヌに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_44"
        else:
            return "2_STORY_MAPPING_43"
    
    def _2_story_mapping_44(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,290), duration=8.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,260), duration=20.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=1.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_45"
        return "2_STORY_MAPPING_44"
    
    def _2_story_mapping_45(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_W_ZONE6"):
                print("MOVEPOINT_TARGET_W_ZONE6")
            if self.image_check("MOVEPOINT_PIC_W_ZONE6"):
                print("MOVEPOINT_PIC_W_ZONE6")
            
        else:
            ret = self.Common_goto(4,0,-1,movepoint_check=1)#ワイルドゾーン6が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_W_ZONE6",pic2="MOVEPOINT_PIC_W_ZONE6") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_46"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_43"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_45"
            else:
                return "2_STORY_MAPPING_45"
        return "2_STORY_MAPPING_45"
    
    def _2_story_mapping_46(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(2,0,2)#ポケセンタープランタンに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_47"
        else:
            return "2_STORY_MAPPING_46"
    
    def _2_story_mapping_47(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,290), duration=8.0, wait=0.5)
            return "2_STORY_MAPPING_48"
        return "2_STORY_MAPPING_47"
    
    def _2_story_mapping_48(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_CAFE_ALAMODE"):
                print("MOVEPOINT_TARGET_CAFE_ALAMODE")
            if self.image_check("MOVEPOINT_PIC_CAFE_ALAMODE"):
                print("MOVEPOINT_PIC_CAFE_ALAMODE")
            
        else:
            ret = self.Common_goto(3,0,0,movepoint_check=1)#カフェアラモードが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_CAFE_ALAMODE",pic2="MOVEPOINT_PIC_CAFE_ALAMODE") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_49"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_46"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_48"
            else:
                return "2_STORY_MAPPING_48"
        return "2_STORY_MAPPING_48"
    
    def _2_story_mapping_49(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(2,0,2)#ポケセンタープランタンに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_50"
        else:
            return "2_STORY_MAPPING_49"
    
    def _2_story_mapping_50(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,0), duration=12.0, wait=0.5)
            return "2_STORY_MAPPING_51"
        return "2_STORY_MAPPING_50"
    
    def _2_story_mapping_51(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_CAFE_TOTO"):
                print("MOVEPOINT_TARGET_CAFE_TOTO")
            if self.image_check("MOVEPOINT_PIC_CAFE_TOTO"):
                print("MOVEPOINT_PIC_CAFE_TOTO")
            
        else:
            ret = self.Common_goto(3,0,3,movepoint_check=1)#カフェトウトウが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_CAFE_TOTO",pic2="MOVEPOINT_PIC_CAFE_TOTO") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_52"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_49"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_51"
            else:
                return "2_STORY_MAPPING_51"
        return "2_STORY_MAPPING_51"
    
    def _2_story_mapping_52(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(4,0,1)#Wゾーン2に移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_53"
        else:
            return "2_STORY_MAPPING_52"
    
    def _2_story_mapping_53(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,5), duration=7.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,70), duration=1.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,300), duration=7.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,50), duration=4.0, wait=0.5)
            return "2_STORY_MAPPING_54"
        return "2_STORY_MAPPING_53"
    
    def _2_story_mapping_54(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_CAFE_TWISTER"):
                print("MOVEPOINT_TARGET_CAFE_TWISTER")
            if self.image_check("MOVEPOINT_PIC_CAFE_TWISTER"):
                print("MOVEPOINT_PIC_CAFE_TWISTER")
            
        else:
            ret = self.Common_goto(3,0,0,movepoint_check=1)#カフェツイスターが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_CAFE_TWISTER",pic2="MOVEPOINT_PIC_CAFE_TWISTER") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_55"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_52"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_54"
            else:
                return "2_STORY_MAPPING_54"
        return "2_STORY_MAPPING_54"
    
    def _2_story_mapping_55(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(2,0,1)#ポケセンターブルーに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_56"
        else:
            return "2_STORY_MAPPING_55"
    
    def _2_story_mapping_56(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=9.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=15.0, wait=0.5)
            self.wait(1.0)

            return "2_STORY_MAPPING_57"
        return "2_STORY_MAPPING_56"
    
    def _2_story_mapping_57(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_CAFE_NUVO2"):
                print("MOVEPOINT_TARGET_CAFE_NUVO2")
            if self.image_check("MOVEPOINT_PIC_CAFE_NUVO2"):
                print("MOVEPOINT_PIC_CAFE_NUVO2")
            
        else:
            ret = self.Common_goto(3,0,-3,movepoint_check=1)#ヌーヴォカフェ2号が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_CAFE_NUVO2",pic2="MOVEPOINT_PIC_CAFE_NUVO2") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_58"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_55"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_57"
            else:
                return "2_STORY_MAPPING_57"
        return "2_STORY_MAPPING_57"
    
    def _2_story_mapping_58(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(4,0,-2)#Wゾーン5に移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_59"
        else:
            return "2_STORY_MAPPING_58"
    
    def _2_story_mapping_59(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,270), duration=4.0, wait=0.5)
            self.wait(1.0)
            return "2_STORY_MAPPING_60"
        return "2_STORY_MAPPING_59"
    
    def _2_story_mapping_60(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_BLUE_SQUARE"):
                print("MOVEPOINT_TARGET_BLUE_SQUARE")
            if self.image_check("MOVEPOINT_PIC_BLUE_SQUARE"):
                print("MOVEPOINT_PIC_BLUE_SQUARE")
            
        else:
            ret = self.Common_goto(1,0,-4,movepoint_check=1)#ブルー広場が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_BLUE_SQUARE",pic2="MOVEPOINT_PIC_BLUE_SQUARE") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_61"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_58"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_60"
            else:
                return "2_STORY_MAPPING_60"
        return "2_STORY_MAPPING_60"
    
    def _2_story_mapping_61(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(2,0,1)#ポケセンターブルーに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_62"
        else:
            return "2_STORY_MAPPING_61"
    
    def _2_story_mapping_62(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,0), duration=3.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,270), duration=0.1, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=14.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,65), duration=14.0, wait=0.5)
            return "2_STORY_MAPPING_63"
        return "2_STORY_MAPPING_62"
    
    def _2_story_mapping_63(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_CAFE_SOLEIL"):
                print("MOVEPOINT_TARGET_BLUE_SQUARE")
            if self.image_check("MOVEPOINT_PIC_BLUE_SQUARE"):
                print("MOVEPOINT_PIC_BLUE_SQUARE")
            
        else:
            ret = self.Common_goto(3,0,-4,movepoint_check=1)#カフェソレイユが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_CAFE_SOLEIL",pic2="MOVEPOINT_PIC_CAFE_SOLEIL") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_65"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_61"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_63"
            else:
                return "2_STORY_MAPPING_63"

        return "2_STORY_MAPPING_63"
    
    def _2_story_mapping_64(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(3,0,-4)#カフェソレイユに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_65"
        else:
            return "2_STORY_MAPPING_64"
    
    def _2_story_mapping_65(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=0.1, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=14.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,75), duration=20.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,300), duration=7.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,330), duration=7.0, wait=0.5)
            return "2_STORY_MAPPING_66"
        return "2_STORY_MAPPING_65"
    
    def _2_story_mapping_66(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_CAFE_FOCUS"):
                print("MOVEPOINT_TARGET_CAFE_FOCUS")
            if self.image_check("MOVEPOINT_PIC_CAFE_FOCUS"):
                print("MOVEPOINT_PIC_CAFE_FOCUS")
            
        else:
            ret = self.Common_goto(3,0,-4,movepoint_check=1)#カフェフォーカスが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_CAFE_FOCUS",pic2="MOVEPOINT_PIC_CAFE_FOCUS") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_67"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_64"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_66"
            else:
                return "2_STORY_MAPPING_66"
        return "2_STORY_MAPPING_66"
    
    def _2_story_mapping_67(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(3,0,-4)#カフェフォーカスに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_68"
        else:
            return "2_STORY_MAPPING_67"
    
    def _2_story_mapping_68(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,200), duration=0.1, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=14.0, wait=0.5)
            self.wait(1.0)
            return "2_STORY_MAPPING_69"
        return "2_STORY_MAPPING_68"
    
    def _2_story_mapping_69(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_CAFE_SLALOM"):
                print("MOVEPOINT_TARGET_CAFE_SLALOM")
            if self.image_check("MOVEPOINT_PIC_CAFE_SLALOM"):
                print("MOVEPOINT_PIC_CAFE_SLALOM")
            
        else:
            ret = self.Common_goto(3,0,-3,movepoint_check=1)#カフェスラロームが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_CAFE_SLALOM",pic2="MOVEPOINT_PIC_CAFE_SLALOM") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_70"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_67"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_69"
            else:
                return "2_STORY_MAPPING_69"
        return "2_STORY_MAPPING_69"
    
    def _2_story_mapping_70(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(2,0,4)#ポケセンターローズ広場に移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_71"
        else:
            return "2_STORY_MAPPING_70"
    
    def _2_story_mapping_71(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,32), duration=14.0, wait=0.5)
            self.wait(1.0)
            return "2_STORY_MAPPING_72"
        return "2_STORY_MAPPING_71"
    
    def _2_story_mapping_72(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_CAFE_NUVO3"):
                print("MOVEPOINT_TARGET_CAFE_NUVO3")
            if self.image_check("MOVEPOINT_PIC_CAFE_NUVO3"):
                print("MOVEPOINT_PIC_CAFE_NUVO3")
            
        else:
            ret = self.Common_goto(3,0,-2,movepoint_check=1)#ヌーヴォカフェ3登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_CAFE_NUVO3",pic2="MOVEPOINT_PIC_CAFE_NUVO3") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_73"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_70"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_72"
            else:
                return "2_STORY_MAPPING_72"
        return "2_STORY_MAPPING_72"
    
    def _2_story_mapping_73(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(2,0,3)#ポケセンターローズに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_74"
        else:
            return "2_STORY_MAPPING_73"
    
    def _2_story_mapping_74(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=24.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,70), duration=8.0, wait=0.5)
            return "2_STORY_MAPPING_75"
        return "2_STORY_MAPPING_74"
    
    def _2_story_mapping_75(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_CAFE_CANCODOR"):
                print("MOVEPOINT_TARGET_CAFE_CANCODOR")
            if self.image_check("MOVEPOINT_PIC_CAFE_CANCODOR"):
                print("MOVEPOINT_PIC_CAFE_CANCODOR")
            
        else:
            ret = self.Common_goto(3,0,-3,movepoint_check=1)#ヌーヴォカフェ3登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_CAFE_CANCODOR",pic2="MOVEPOINT_PIC_CAFE_CANCODOR") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_76"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_73"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_75"
            else:
                return "2_STORY_MAPPING_75"
        return "2_STORY_MAPPING_75"
    
    def _2_story_mapping_76(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(2,0,-3)#ポケセンターメディオに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_77"
        else:
            return "2_STORY_MAPPING_76"
    
    def _2_story_mapping_77(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,300), duration=12.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,218), duration=50.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,125), duration=4.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_78"
        return "2_STORY_MAPPING_77"
    
    def _2_story_mapping_78(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_RESTAURANT_2RYU"):
                print("MOVEPOINT_TARGET_RESTAURANT_2RYU")
            if self.image_check("MOVEPOINT_PIC_RESTAURANT_2RYU"):
                print("MOVEPOINT_PIC_RESTAURANT_2RYU")
            
        else:
            ret = self.Common_goto(1,0,-2,movepoint_check=1)#リストランテニリューが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_RESTAURANT_2RYU",pic2="MOVEPOINT_PIC_RESTAURANT_2RYU") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_79"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_76"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_78"
            else:
                return "2_STORY_MAPPING_78"
        return "2_STORY_MAPPING_78"
    
    def _2_story_mapping_79(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(2,0,-4)#ポケセンタールージュに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_80"
        else:
            return "2_STORY_MAPPING_79"
    
    def _2_story_mapping_80(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,185), duration=18.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,270), duration=5.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_81_0"
        return "2_STORY_MAPPING_80"
    
    def _2_story_mapping_81_0(self):
        #Common_gotoでアイコン判定していないため
        if self.image_check("WANINOKO_ICON") or self.image_check("MERIP_ICON_GET5"):
            self.press(Direction(Stick.LEFT,270), duration=1.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_81"
        return "2_STORY_MAPPING_81_0"
    
    def _2_story_mapping_81(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_ART_MUSEUM"):
                print("MOVEPOINT_TARGET_ART_MUSEUM")
            if self.image_check("MOVEPOINT_PIC_ART_MUSEUM"):
                print("MOVEPOINT_PIC_ART_MUSEUM")
            
        else:
            ret = self.Common_goto(1,0,-3,movepoint_check=1)#ミアレ美術館が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_ART_MUSEUM",pic2="MOVEPOINT_PIC_ART_MUSEUM") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_83"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_79"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_81"
            else:
                return "2_STORY_MAPPING_81"
        return "2_STORY_MAPPING_81"
    
    def _2_story_mapping_82(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(1,0,-3)#ミアレ美術館に移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_83"
        else:
            return "2_STORY_MAPPING_82"
    
    def _2_story_mapping_83(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,350), duration=29.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,80), duration=5.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_84"
        return "2_STORY_MAPPING_83"
    
    def _2_story_mapping_84(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_HOTEL_SURREALISH"):
                print("MOVEPOINT_TARGET_HOTEL_SURREALISH")
            if self.image_check("MOVEPOINT_PIC_HOTEL_SURREALISH"):
                print("MOVEPOINT_PIC_HOTEL_SURREALISH")
            
        else:
            ret = self.Common_goto(1,0,-5,movepoint_check=1)#ホテルシューリッシュが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_HOTEL_SURREALISH",pic2="MOVEPOINT_PIC_HOTEL_SURREALISH") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_86"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_82"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_84"
            else:
                return "2_STORY_MAPPING_84"
        return "2_STORY_MAPPING_84"
    
    def _2_story_mapping_85(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(1,0,-5)#ホテルシューリッシュに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_86"
        else:
            return "2_STORY_MAPPING_85"
    
    def _2_story_mapping_86(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,340), duration=19.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_87"
        return "2_STORY_MAPPING_86"
    
    def _2_story_mapping_87(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_CAFE_ULT"):
                print("MOVEPOINT_TARGET_CAFE_ULT")
            if self.image_check("MOVEPOINT_PIC_CAFE_ULT"):
                print("MOVEPOINT_PIC_CAFE_ULT")
            
        else:
            ret = self.Common_goto(3,0,-2,movepoint_check=1)#カフェアルティメットが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_CAFE_ULT",pic2="MOVEPOINT_PIC_CAFE_ULT") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_88"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_85"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_87"
            else:
                return "2_STORY_MAPPING_87"
        return "2_STORY_MAPPING_87"
    
    def _2_story_mapping_88(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(2,0,-1)#ポケセンターイベールに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_89"
        else:
            return "2_STORY_MAPPING_88"
    
    def _2_story_mapping_89(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,300), duration=8.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=5.0, wait=0.5)
            self.wait(1.0)
            return "2_STORY_MAPPING_90"
        return "2_STORY_MAPPING_89"
    
    def _2_story_mapping_90(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_CAFE_PARTENAIRE"):
                print("MOVEPOINT_TARGET_CAFE_PARTENAIRE")
            if self.image_check("MOVEPOINT_PIC_CAFE_PARTENAIRE"):
                print("MOVEPOINT_PIC_CAFE_PARTENAIRE")
            
        else:
            ret = self.Common_goto(3,0,-1,movepoint_check=1)#カフェパルトネールが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_CAFE_PARTENAIRE",pic2="MOVEPOINT_PIC_CAFE_PARTENAIRE") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_91"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_88"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_90"
            else:
                return "2_STORY_MAPPING_90"
        return "2_STORY_MAPPING_90"
    
    def _2_story_mapping_91(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(2,0,-2)#ポケセンタージョーヌに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_92"
        else:
            return "2_STORY_MAPPING_91"
    
    def _2_story_mapping_92(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,300), duration=14.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,260), duration=14.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,240), duration=11.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_93"
        return "2_STORY_MAPPING_92"
    
    def _2_story_mapping_93(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,340), duration=5.0, wait=0.5)
            self.wait(1.0)
            return "2_STORY_MAPPING_94"
        return "2_STORY_MAPPING_93"
    
    def _2_story_mapping_94(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_CAFE_BATAILLE"):
                print("MOVEPOINT_TARGET_CAFE_BATAILLE")
            if self.image_check("MOVEPOINT_PIC_CAFE_BATAILLE"):
                print("MOVEPOINT_PIC_CAFE_BATAILLE")
            
        else:
            ret = self.Common_goto(3,0,-1,movepoint_check=1)#カフェバタイユが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_CAFE_BATAILLE",pic2="MOVEPOINT_PIC_CAFE_BATAILLE") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_95"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_91"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_94"
            else:
                return "2_STORY_MAPPING_94"
        return "2_STORY_MAPPING_94"
    
    def _2_story_mapping_95(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(2,0,0)#ポケセンターベールに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_96"
        else:
            return "2_STORY_MAPPING_95"
    
    def _2_story_mapping_96(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,350), duration=10.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,10), duration=15.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,100), duration=5.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_97"
        return "2_STORY_MAPPING_96"
    
    def _2_story_mapping_97(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_RACINE"):
                print("MOVEPOINT_TARGET_RACINE")
            if self.image_check("MOVEPOINT_PIC_RACINE"):
                print("MOVEPOINT_PIC_CRACINE")
            
        else:
            ret = self.Common_goto(1,0,4,movepoint_check=1)#ラシーヌ工務店が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_RACINE",pic2="MOVEPOINT_PIC_RACINE") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_99"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_95"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_97"
            else:
                return "2_STORY_MAPPING_97"
        return "2_STORY_MAPPING_97"
    
    def _2_story_mapping_98(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(1,0,4)#ラシーヌ工務店に移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_99"
        else:
            return "2_STORY_MAPPING_98"
    
    def _2_story_mapping_99(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,350), duration=10.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,10), duration=13.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,100), duration=6.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,10), duration=2.5, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,280), duration=3.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_100"
        return "2_STORY_MAPPING_99"
    
    def _2_story_mapping_100(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_RESTAURANT_DOHUTSU"):
                print("MOVEPOINT_TARGET_RESTAURANT_DOHUTSU")
            if self.image_check("MOVEPOINT_PIC_RESTAURANT_DOHUTSU"):
                print("MOVEPOINT_PIC_RESTAURANT_DOHUTSU")
            
        else:
            ret = self.Common_goto(1,0,5,movepoint_check=1)#レストランドフツーが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_RESTAURANT_DOHUTSU",pic2="MOVEPOINT_PIC_RESTAURANT_DOHUTSU") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_101"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_98"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_100"
            else:
                return "2_STORY_MAPPING_100"
        return "2_STORY_MAPPING_100"
    
    def _2_story_mapping_101(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(2,0,-3)#ポケセンターメディオに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_102"
        else:
            return "2_STORY_MAPPING_101"
    
    def _2_story_mapping_102(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,0), duration=3.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,60), duration=20.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,0), duration=6.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,75), duration=12.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,160), duration=9.5, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,75), duration=5.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,310), duration=8.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_103"
        return "2_STORY_MAPPING_102"
    
    def _2_story_mapping_103(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_JUSTICE_DOJO"):
                print("MOVEPOINT_TARGET_JUSTICE_DOJO")
            if self.image_check("MOVEPOINT_PIC_JUSTICE_DOJO"):
                print("MOVEPOINT_PIC_JUSTICE_DOJO")
            
        else:
            ret = self.Common_goto(1,0,-1,movepoint_check=1)#ジャスティス道場が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_JUSTICE_DOJO",pic2="MOVEPOINT_PIC_JUSTICE_DOJO") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_104"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_101"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_103"
            else:
                return "2_STORY_MAPPING_103"
        return "2_STORY_MAPPING_103"
    
    def _2_story_mapping_104(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(4,0,2)#Wゾーン2に移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_105"
        else:
            return "2_STORY_MAPPING_104"
    
    def _2_story_mapping_105(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,15), duration=11.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,330), duration=20.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,0), duration=2.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=10.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,270), duration=0.5, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=1.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_106"
        return "2_STORY_MAPPING_105"
    
    def _2_story_mapping_106(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_RESTAURANT_EXTREAME"):
                print("MOVEPOINT_TARGET_RESTAURANT_EXTREAME")
            if self.image_check("MOVEPOINT_PIC_RESTAURANT_EXTREAME"):
                print("MOVEPOINT_PIC_RESTAURANT_EXTREAME")
            
        else:
            ret = self.Common_goto(1,0,-2,movepoint_check=1)#レストランドキワミが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_RESTAURANT_EXTREAME",pic2="MOVEPOINT_PIC_RESTAURANT_EXTREAME") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_107"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_104"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_106"
            else:
                return "2_STORY_MAPPING_106"
        return "2_STORY_MAPPING_106"
    
    def _2_story_mapping_107(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(1,0,-4)#レストランニリューに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_108"
        else:
            return "2_STORY_MAPPING_107"
    
    def _2_story_mapping_108(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,330), duration=15.0, wait=0.5)
            return "2_STORY_MAPPING_109"
        return "2_STORY_MAPPING_108"
    
    def _2_story_mapping_109(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_CAFE_CUTE"):
                print("MOVEPOINT_TARGET_CAFE_CUTE")
            if self.image_check("MOVEPOINT_PIC_CAFE_CUTE"):
                print("MOVEPOINT_PIC_CAFE_CUTE")
            
        else:
            ret = self.Common_goto(3,1,1,movepoint_check=1)#カフェかわいがりが登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_CAFE_CUTE",pic2="MOVEPOINT_PIC_CAFE_CUTE") == True:
                    self.Common_goto_jump()
                    return "2_STORY_TOWER_47"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_107"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_109"
            else:
                return "2_STORY_MAPPING_109"
        return "2_STORY_MAPPING_109"
        
    
    def _2_story_tower_47(self):
        #ヘラクロス交換
        ### AUTO_SAVE_POINT
        ret = self.Common_goto(2,0,5)#ポケセンルージュに移動で位置確定
        if ret == "START":
            return "2_STORY_TOWER_48"
        else:
            return "2_STORY_TOWER_47"
    
    def _2_story_tower_48(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,350), duration=3.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,110), duration=8.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=5.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=0.3, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_TOWER_49"
        return "2_STORY_TOWER_48"
    
    def _2_story_tower_49(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT"):
                return "2_STORY_TOWER_50"
        return "2_STORY_TOWER_49"
    
    def _2_story_tower_50(self):
        ### AUTO_SAVE_POINT
        if self.check_picture==1:
            if self.image_check("PIKA_ICON_BOX6"):
                print("PIKA_ICON_BOX6")
            return "2_STORY_TOWER_50"
        else:
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                self.wait(1.0)
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_TOWER_51"
            return "2_STORY_TOWER_50"
    
    def _2_story_tower_51(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT",sub2_button="A",sub2_picture="PIKA_ICON_BOX6",sleeptime=2.0):
                self.wait(1.0)
                if self.image_check("SIDE_MARKER_CENTER_WIDE"):
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                else:
                    return "2_STORY_TOWER_52"
        return "2_STORY_TOWER_51"
    
    def _2_story_tower_52(self):
        ### AUTO_SAVE_POINT
        ret = self.Common_goto(4,0,-3)#Wゾーン4に移動で位置確定
        if ret == "START":
            return "2_STORY_TOWER_53"
        else:
            return "2_STORY_TOWER_52"
    
    def _2_story_tower_53(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,45), duration=0.8, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_TOWER_54"
        return "2_STORY_TOWER_53"
    
    def _2_story_tower_54(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT"):
                return "2_STORY_TOWER_55"
            
        for i in range(10):
            self.wait(0.5)
            if self.image_check("TEXT_WHITE_COMMENT"):
                if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT"):
                    return "2_STORY_TOWER_55"
        return "2_STORY_TOWER_52"
    
    def _2_story_tower_55(self): 
        ### AUTO_SAVE_POINT
        if self.check_picture==1:
            if self.image_check("SIDE_SELECT_TOP_MAP"):
                print("SIDE_SELECT_TOP_MAP")
            return "2_STORY_TOWER_55"
        else:
            ret = self.Common_goto(4,0,-3)#Wゾーン4に移動で位置確定
            if ret == "START":
                return "2_STORY_TOWER_56"
            else:
                return "2_STORY_TOWER_55"
    
    def _2_story_tower_56(self): 
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_TOWER_57"
        return "2_STORY_TOWER_56"
    
    def _2_story_tower_57(self): 
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=14.0, wait=0.5)
            self.press(Direction(Stick.LEFT,110), duration=6.5, wait=0.5)
            self.press(Direction(Stick.LEFT,180), duration=1.8, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "2_STORY_TOWER_58"
        return "2_STORY_TOWER_57"
    
    def _2_story_tower_58(self): 
        if self.image_check("TEXT_BLACK_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="ESCAPE",sub_button="A",sub_picture="2_SELECT"):
                return "2_STORY_TOWER_59"
        elif self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            return "2_STORY_TOWER_55"
        return "2_STORY_TOWER_58"
    
    def _2_story_tower_59(self):
        if self.image_check("ESCAPE"):
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                if self.image_check("FIELD_W"):
                    self.etc_sendCommand("Lbutton_up")
            self.battle_coCp_noloop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            return "2_STORY_TOWER_60"
        return "2_STORY_TOWER_59"
    
    def _2_story_tower_60(self):
        if self.image_check("TEXT_BLACK_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT",sub2_button="A",sub2_picture="TEXT_BLACK_COMMENT"):
                return "2_STORY_TOWER_61"
        return "2_STORY_TOWER_60"
    
    def _2_story_tower_61(self): 
        ret = self.Common_goto(4,0,-3)#Wゾーン4に移動で位置確定
        if ret == "START":
            return "2_STORY_TOWER_62"
        else:
            return "2_STORY_TOWER_61"
    
    def _2_story_tower_62(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,45), duration=0.9, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_TOWER_63"
        return "2_STORY_TOWER_62"
    
    def _2_story_tower_63(self): 
        if self.story_Template_Comment_Out():
            return "2_STORY_TOWER_64"
        return "2_STORY_TOWER_61"
    
    def _2_story_tower_64(self): 
        ### AUTO_SAVE_POINT
        ret = self.Common_goto(2,0,5)#ポケセンルージュに移動で位置確定
        if ret == "START":
            return "2_STORY_TOWER_65"
        else:
            return "2_STORY_TOWER_64"
    
    def _2_story_tower_65(self):
        if self.Common_pokemon_recovery():
            return "2_STORY_TOWER_66"
        return "2_STORY_TOWER_65"
    
    def _2_story_tower_66(self):
        #親分クエスト
        ### AUTO_SAVE_POINT
        ret = self.Common_goto(4,0,2)#Wゾーン3に移動で位置確定
        if ret == "START":
            return "2_STORY_TOWER_67"
        else:
            return "2_STORY_TOWER_66"
    
    def _2_story_tower_67(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,25), duration=13.5, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,86), duration=5.5, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "2_STORY_TOWER_68"
        return "2_STORY_TOWER_67"
    
    def _2_story_tower_68(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT"):
                return "2_STORY_TOWER_69"
        return "2_STORY_TOWER_68"
    
    def _2_story_tower_69(self):
        ### AUTO_SAVE_POINT
        ret = self.Common_goto(1,0,-3)#ローリングドリーマーに移動で位置確定
        if ret == "START":
            return "2_STORY_TOWER_70"
        else:
            return "2_STORY_TOWER_69"
    
    def _2_story_tower_70(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,180), duration=3.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=37.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,190), duration=8.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=0.5, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,260), duration=7.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,220), duration=10.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,35), duration=3.3, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "2_STORY_TOWER_71"
        return "2_STORY_TOWER_70"
    
    def _2_story_tower_71(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",endpicture3="ESCAPE",sub_button="A",sub_picture="2_SELECT",sleeptime=1.0):
                return "2_STORY_TOWER_72"

        for i in range(10):
            self.wait(0.5)
            if self.image_check("TEXT_WHITE_COMMENT"):
                if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",endpicture3="ESCAPE",sub_button="A",sub_picture="2_SELECT",sleeptime=1.0):
                    return "2_STORY_TOWER_72"
        return "2_STORY_TOWER_69"
    
    def _2_story_tower_72(self):
        return self.story_Template_battle_function(bkprg_ret="2_STORY_TOWER_71",prg_ret="2_STORY_TOWER_73",noprg_ret="2_STORY_TOWER_72",Xaction=1,Aaction=1,Yaction=0,Baction=1,lockon_endskip=0,get_chanceicon4=0,noCp=1,markertype=1,battle_mode=1)

        #親分ホルビーが必要な場合はゲットマーカー4でゲット処理を追加
        #敗戦対応が必要なはず
        #移動なしでも行けるので一旦プレイヤー移動なしで実施
        if self.image_check("ESCAPE"):
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                if self.image_check("FIELD_W"):
                    self.etc_sendCommand("Lbutton_up")
            self.battle_coCp_noloop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("HELP_MARKER"):
            self.press(Direction(Stick.LEFT,90), duration=0.7, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "2_STORY_TOWER_71"
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_TOWER_72"
        elif self.image_check("TEXT_WHITE_COMMENT"):
            return "2_STORY_TOWER_73"

        return "2_STORY_TOWER_72"
    
    def _2_story_tower_73(self): 
        return self.story_Template_battle_after(bkprg_ret="2_STORY_TOWER_72",prg_ret="2_STORY_TOWER_74")

        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT"):
                return "2_STORY_TOWER_74"
        return "2_STORY_TOWER_73"

    def _2_story_tower_74(self): 
        ### AUTO_SAVE_POINT
        ret = self.Common_goto(2,0,5)#ポケセンルージュに移動で位置確定
        if ret == "START":
            return "2_STORY_TOWER_75"
        else:
            return "2_STORY_TOWER_74"
    
    def _2_story_tower_75(self):
        if self.Common_pokemon_recovery():
            return "2_STORY_TOWER_76"
        return "2_STORY_TOWER_75"
    
    def _2_story_tower_76(self): 
        ### AUTO_SAVE_POINT
        ret = self.Common_goto(1,0,-6)#ハンサムハウスに移動で位置確定
        if ret == "START":
            return "2_STORY_TOWER_77"
        else:
            return "2_STORY_TOWER_76"
    
    def _2_story_tower_77(self): 
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "2_STORY_TOWER_78"
        return "2_STORY_TOWER_77"
    
    def _2_story_tower_78(self): 
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="WANINOKO_ICON",endpicture2="MERIP_ICON_GET5",sub_button="A",sub_picture="2_SELECT"):
                return "2_STORY_TOWER_79"
        return "2_STORY_TOWER_78"
    
    def _2_story_tower_79(self): 
        if self.image_check("WANINOKO_ICON") or self.image_check("MERIP_ICON_GET5"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "2_STORY_TOWER_80"    
        return "2_STORY_TOWER_79"
    
    def _2_story_tower_80(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,145), duration=3.8, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "2_STORY_TOWER_81"  
        return "2_STORY_TOWER_80"
    
    def _2_story_tower_81(self): 
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="ESCAPE",sub_button="A",sub_picture="2_SELECT"):
                return "2_STORY_TOWER_82"
        return "2_STORY_TOWER_81"
    
    def _2_story_tower_82(self):
        if self.image_check("ESCAPE"):
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                if self.image_check("FIELD_W"):
                    self.etc_sendCommand("Lbutton_up")
            self.battle_coCp_noloop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_WHITE_COMMENT"):
            return "2_STORY_TOWER_83"
        return "2_STORY_TOWER_82"
    
    def _2_story_tower_83(self): 
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="WANINOKO_ICON",endpicture2="MERIP_ICON_GET5",sub_button="A",sub_picture="2_SELECT"):
                return "2_STORY_TOWER_84"
        return "2_STORY_TOWER_83"
    
    def _2_story_tower_84(self):
        ret = self.Common_change_time_set(check_timing="NIGHT")#時間変更前のためとりあえず時間変更とする
        if ret == "START":
            return "2_STORY_Y_LANK_BATTLE_ZONE"
        else:
            return "2_STORY_TOWER_84"
        
    
    def _2_story_y_lank_battle_zone(self):
        self.battle_zone_loop_num = 1
        self.no_Cplus=1
        self.za_infi_main_current_state = self.STATE_ZA_INFI_MAIN_FUNCTION[self.za_infi_main_current_state]()
        self.wait(self.SLEEPLIST[9][2])
        if self.za_infi_main_current_state == "ZA_INFI_QUASAR_LOOP":
            self.za_infi_main_current_state = "ZA_INFI_MAIN_START"
            return "2_STORY_Y_LANK_MOVE1"
        else: 
            return "2_STORY_Y_LANK_BATTLE_ZONE"
    
    def _2_story_y_lank_move0(self):
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "2_STORY_Y_LANK_MOVE1"
        else:
            return "2_STORY_Y_LANK_MOVE0"
    
    def _2_story_y_lank_move1(self):
        ret = self.Common_goto(4,0,-2)#Wゾーン5側から
        if ret == "START":
            return "2_STORY_Y_LANK_MOVE2"
        else:
            return "2_STORY_Y_LANK_MOVE1"

    def _2_story_y_lank_move2(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,350), duration=5.5, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,233), duration=0.5, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=8.5, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_Y_LANK_MOVE3"
        return "2_STORY_Y_LANK_MOVE2"

    def _2_story_y_lank_move3(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="BATTLE_BALL_CHECK",endpicture2="ESCAPE",sub_button="A",sub_picture="3_SELECT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                return "2_STORY_Y_LANK_MOVE4"
        for i in range(10):
            self.wait(0.5)
            if self.image_check("TEXT_WHITE_COMMENT"):
                if self.renda_button(rendabutton="B",endpicture="BATTLE_BALL_CHECK",endpicture2="ESCAPE",sub_button="A",sub_picture="3_SELECT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER"):
                    return "2_STORY_Y_LANK_MOVE4"
        return "2_STORY_Y_LANK_MOVE0"

    #Yランク
    def _2_story_y_lank_move4(self):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE") or self.image_check("TEXT_WHITE_COMMENT"):
            self.battle_coCp_noloop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=0.5, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_Y_LANK_MOVE3"
        elif self.image_check("COIN_ICON"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_Y_LANK_MOVE5"
        return "2_STORY_Y_LANK_MOVE4"

    def _2_story_y_lank_move5(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="IN_ICON",sub_button="A",sub_picture="3_SELECT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="HELP_MARKER",sub4_button="A",sub4_picture="MORNING"):
                self.wait(1.0)
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_Y_END"
        return "2_STORY_Y_LANK_MOVE5"

    def _2_story_y_end(self):
        return "2_STORY_X_LANK_MOVE1"

    def _2_story_x_lank_move1(self):
        if self.image_check("IN_ICON"):
            self.press(Direction(Stick.LEFT,100), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_X_LANK_MOVE2"
        return "2_STORY_X_LANK_MOVE1"
    
    def _2_story_x_lank_move2(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_X_LANK_MOVE3"
        return "2_STORY_X_LANK_MOVE2"
    
    def _2_story_x_lank_move3(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="BATTLE_BALL_CHECK",endpicture2="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sleeptime=0.5):
                return "2_STORY_X_LANK_MOVE4"
        return "2_STORY_X_LANK_MOVE3"
    
    def _2_story_x_lank_move4(self):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE") or self.image_check("TEXT_WHITE_COMMENT"):
            self.battle_coCp_noloop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            for i in range(10):
                self.wait(1.0)
                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                    self.press(Direction(Stick.LEFT,90), duration=0.5, wait=0.5)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_X_LANK_MOVE3"
        elif self.image_check("COIN_ICON"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_X_LANK_MOVE5"

        return "2_STORY_X_LANK_MOVE4"
    
    def _2_story_x_lank_move5(self):
        if self.image_check("COIN_ICON") or self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT"):
                return "2_STORY_X_LANK_MOVE6"
        return "2_STORY_X_LANK_MOVE5"

    def _2_story_x_lank_move6(self):
        #スボミーイベントを想定外に発生しないために処理
        ret = self.Common_goto(2,0,2)#ポケセンタープランタンへ移動
        if ret == "START":
            return "2_STORY_X_LANK_MOVE7"
        else:
            return "2_STORY_X_LANK_MOVE6"
        
    def _2_story_x_lank_move7(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=4.0, wait=1.0)
            self.wait(0.5)
            return "2_STORY_X_LANK_MOVE8"
        return "2_STORY_X_LANK_MOVE7"

    def _2_story_x_lank_move8(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sleeptime=0.5):
                return "2_STORY_X_LANK_BATTLE_ZONE"
        return "2_STORY_X_LANK_MOVE8"

    def _2_story_x_lank_battle_zone(self):
        self.battle_zone_loop_num = 1
        self.no_Cplus=1
        self.za_infi_main_current_state = self.STATE_ZA_INFI_MAIN_FUNCTION[self.za_infi_main_current_state]()
        self.wait(self.SLEEPLIST[9][2])
        if self.za_infi_main_current_state == "ZA_INFI_QUASAR_LOOP":
            self.za_infi_main_current_state = "ZA_INFI_MAIN_START"
            return "2_STORY_X_LANK_MOVE9"
        else: 
            return "2_STORY_X_LANK_BATTLE_ZONE"

    def _2_story_x_lank_move9(self):
        ret = self.Common_goto(1,0,-2)#レストランドキワミへ移動
        if ret == "START":
            return "2_STORY_X_LANK_MOVE10"
        else:
            return "2_STORY_X_LANK_MOVE9"
    
    def _2_story_x_lank_move10(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            
            self.press(Direction(Stick.LEFT,4), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,75), duration=6.5, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,0), duration=0.1, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=14.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,280), duration=0.4, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_X_LANK_MOVE11"
        return "2_STORY_X_LANK_MOVE10"
    
    def _2_story_x_lank_move11(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="BATTLE_BALL_CHECK",endpicture2="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.5):
                return "2_STORY_X_LANK_MOVE12"
        return "2_STORY_X_LANK_MOVE11"
    
    def _2_story_x_lank_move12(self):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE") or self.image_check("TEXT_WHITE_COMMENT"):
            self.battle_coCp_noloop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            for i in range(10):
                self.wait(1.0)
                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                    #self.press(Direction(Stick.LEFT,90), duration=0.5, wait=0.5)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_X_LANK_MOVE11"
                elif self.image_check("TEXT_BLACK_COMMENT"):
                    return "2_STORY_X_LANK_MOVE11"
        elif self.image_check("EVENT_MARKER_CENTER_WIDE"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_X_LANK_MOVE11"
        elif self.image_check("TEXT_GREEN_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="BATTLE_BALL_CHECK",endpicture2="ESCAPE",endpicture3="EVENT_MARKER_CENTER_WIDE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.5):
                return "2_STORY_X_LANK_MOVE12"
        elif self.image_check("COIN_ICON"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_X_LANK_MOVE13"
        return "2_STORY_X_LANK_MOVE12"
    
    def _2_story_x_lank_move13(self):
        if self.image_check("COIN_ICON") or self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT",sub2_button="A",sub2_picture="MORNING"):
                return "2_STORY_W_LANK_MOVE1"
        return "2_STORY_X_LANK_MOVE13"
    
    def _2_story_w_lank_move1(self):
        ret = self.Common_goto(4,0,1)#Wゾーン2へ移動
        if ret == "START":
            return "2_STORY_W_LANK_MOVE2"
        else:
            return "2_STORY_W_LANK_MOVE1"
    
    def _2_story_w_lank_move2(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            
            self.press(Direction(Stick.LEFT,170), duration=11.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,270), duration=7.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,200), duration=1.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,270), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,0), duration=0.1, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=14.0, wait=1.0)
            self.wait(0.5)

            return "2_STORY_W_LANK_MOVE3"
        return "2_STORY_W_LANK_MOVE2"
    
    def _2_story_w_lank_move3(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="BATTLE_BALL_CHECK",endpicture2="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sleeptime=0.5):
                return "2_STORY_W_LANK_MOVE4"
        return "2_STORY_W_LANK_MOVE3"
    
    def _2_story_w_lank_move4(self):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE") or self.image_check("TEXT_WHITE_COMMENT"):
            self.battle_coCp_noloop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            for i in range(10):
                self.wait(1.0)
                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                    self.press(Direction(Stick.LEFT,75), duration=4.0, wait=0.5)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_W_LANK_MOVE3"
                elif self.image_check("TEXT_BLACK_COMMENT"):
                    return "2_STORY_W_LANK_MOVE3"
        elif self.image_check("EVENT_MARKER_CENTER_WIDE"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_W_LANK_MOVE3"
        elif self.image_check("TEXT_GREEN_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="BATTLE_BALL_CHECK",endpicture2="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sleeptime=0.5):
                "2_STORY_W_LANK_MOVE4"
        elif self.image_check("COIN_ICON"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_W_LANK_MOVE5"
        return "2_STORY_W_LANK_MOVE4"
    
    def _2_story_w_lank_move5(self):
        if self.image_check("COIN_ICON") or self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT",sub2_button="A",sub2_picture="HELP_MARKER"):
                return "2_STORY_W_LANK_MOVE6"
        return "2_STORY_W_LANK_MOVE5"
    
    #ヒトカゲの対策を先にした方がよい？(回復はしないが通る)
    def _2_story_w_lank_move6(self):
        ret = self.Common_goto(2,0,2)#ポケセンタープランタンへ移動
        if ret == "START":
            return "2_STORY_W_LANK_MOVE7"
        else:
            return "2_STORY_W_LANK_MOVE6"
    
    def _2_story_w_lank_move7(self):
        if self.Common_pokemon_recovery():
            return "2_STORY_W_LANK_BATTLE_ZONE"
        return "2_STORY_W_LANK_MOVE7"
    
    def _2_story_w_lank_battle_zone(self):
        self.battle_zone_loop_num = 1
        self.no_Cplus=1
        self.za_infi_main_current_state = self.STATE_ZA_INFI_MAIN_FUNCTION[self.za_infi_main_current_state]()
        self.wait(self.SLEEPLIST[9][2])
        if self.za_infi_main_current_state == "ZA_INFI_QUASAR_LOOP":
            self.za_infi_main_current_state = "ZA_INFI_MAIN_START"
            return "2_STORY_W_LANK_MOVE8"
        else: 
            return "2_STORY_W_LANK_BATTLE_ZONE"
    
    def _2_story_w_lank_move8(self):
        ret = self.Common_goto(1,0,5)#レストランドフツーへ移動
        if ret == "START":
            return "2_STORY_W_LANK_MOVE9"
        else:
            return "2_STORY_W_LANK_MOVE8"
    
    def _2_story_w_lank_move9(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(0.5)
            return "2_STORY_W_LANK_MOVE10"
        return "2_STORY_W_LANK_MOVE9"
    
    def _2_story_w_lank_move10(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,0), duration=0.3, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(0.5)
            return "2_STORY_W_LANK_MOVE11"
        return "2_STORY_W_LANK_MOVE10"
    
    def _2_story_w_lank_move11(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="BATTLE_BALL_CHECK",endpicture2="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.5):
                return "2_STORY_W_LANK_MOVE12"
        for i in range(10):
            self.wait(0.5)
            if self.image_check("TEXT_WHITE_COMMENT"):
                if self.renda_button(rendabutton="B",endpicture="BATTLE_BALL_CHECK",endpicture2="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.5):
                    return "2_STORY_W_LANK_MOVE12"
        return "2_STORY_W_LANK_MOVE8"
    
    def _2_story_w_lank_move12(self):
        if self.image_check("W_BATTLE_END"):
            return "2_STORY_W_LANK_MOVE13"
        elif self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE") or self.image_check("TEXT_WHITE_COMMENT"):
            self.battle_coCp_noloop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            for i in range(10):
                self.wait(1.0)
                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                    self.press(Direction(Stick.LEFT,90), duration=0.1, wait=0.5)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_W_LANK_MOVE11"
                elif self.image_check("TEXT_BLACK_COMMENT"):
                    return "2_STORY_W_LANK_MOVE11"
        elif self.image_check("EVENT_MARKER_CENTER_WIDE"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_W_LANK_MOVE11"
        elif self.image_check("COIN_ICON"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_W_LANK_MOVE13"
        else:#想定外の復帰用
            if self.renda_button(rendabutton="B",endpicture="TEXT_WHITE_COMMENT",endpicture2="BATTLE_BALL_CHECK",endpicture3="COIN_ICON",endpicture4="EVENT_MARKER_CENTER_WIDE",endpicture5="W_BATTLE_END",sub_button="A",sub_picture="2_SELECT",sub2_button="A",sub2_picture="HELP_MARKER"):
                if self.image_check("COIN_ICON"):
                    return "2_STORY_W_LANK_MOVE13"
                return "2_STORY_W_LANK_MOVE12"
        return "2_STORY_W_LANK_MOVE12"
    #check
    def _2_story_w_lank_move13(self):
        if self.image_check("W_BATTLE_END"):
            return "2_STORY_ABSOL_MOVE1"
        elif self.image_check("COIN_ICON") or self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="2_SELECT",sub2_button="A",sub2_picture="HELP_MARKER"):
                return "2_STORY_ABSOL_MOVE1"
        return "2_STORY_W_LANK_MOVE13"
    
    #リセットでしか戻れない・緑のコメントで戻した方がよい
    def _2_story_absol_move1(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,60), duration=4.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,0), duration=5.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,270), duration=7.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,0), duration=6.5, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,95), duration=15.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,100), duration=7.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=10.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,0), duration=15.0, wait=1.0)
            self.wait(0.5)
            return "2_STORY_ABSOL_MOVE2"
        return "2_STORY_ABSOL_MOVE1"
    
    def _2_story_absol_move2(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_ABSOL_BATTLE"
        return "2_STORY_ABSOL_MOVE2"

    def _2_story_absol_battle(self):
        if self.mega_evolution_battle_mode_select(mode=0):
            return "2_STORY_ABSOL_MOVE3"   
        return "2_STORY_ABSOL_BATTLE"
    
    def _2_story_absol_move3(self):
        if self.story_Template_Comment_Out():
                return "2_STORY_ABSOL_MOVE4"
        return "2_STORY_ABSOL_MOVE3"
            
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.5):
                return "2_STORY_ABSOL_MOVE4"
        elif self.image_check("MORNING"):
            self.pressRep(Button.A, repeat=5, duration=0.15, wait=0.5, interval=0.1)
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.5):
                return "2_STORY_ABSOL_MOVE4"
        return "2_STORY_ABSOL_MOVE3" 
    
    def _2_story_absol_move4(self):
        ### AUTO_SAVE_POINT
        if self.check_picture==1:
            if self.image_check("BOXWINDOW"):
                print("BOXWINDOW")
            if self.image_check("BOXMENU"):
                print("BOXMENU")
        else:
            if self.image_check("IN_ICON"):
                self.press(Direction(Stick.LEFT,100), duration=3.0, wait=1.0)
                self.wait(0.5)
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_BOX_CHANGE1"
        return "2_STORY_ABSOL_MOVE4"
    
    def _2_story_box_change1(self):
        #アブソルと入れ替え
        self.common_box_change_current_state = self.common_box_change_function(target1=0,target2=3,target1_high=0,target2_high=-1)
        if self.common_box_change_current_state == "COMMON_BOX_CHANGE_START":
            return "2_STORY_ITEM_GIVE1"
            #return "2_STORY_BOX_CHANGE2"
        else:
            return "2_STORY_BOX_CHANGE1"
        
    def _2_story_box_change2(self):
        self.common_box_change_current_state = self.common_box_change_function(target1=4,target2=1,target1_high=-1,target2_high=0)
        if self.common_box_change_current_state == "COMMON_BOX_CHANGE_START":
            return "2_STORY_ITEM_GIVE1"
        else:
            return "2_STORY_BOX_CHANGE2"
    
    def _2_story_item_give1(self):
        self.common_item_give_current_state = self.common_item_give_function(selectnum=4,target1=4,target2=0)
        if self.common_item_give_current_state == "COMMON_ITEM_GIVE_START":
            return "2_STORY_ABSOL_MOVE5"
        else:
            return "2_STORY_ITEM_GIVE1"

    def _2_story_absol_move5(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=3.0, wait=1.0)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_ABSOL_MOVE6"
        return "2_STORY_ABSOL_MOVE5"
    
    def _2_story_absol_move6(self):
        return self.story_Template_battle_before(noprg_ret="2_STORY_ABSOL_MOVE6",prg_ret="2_STORY_ABSOL_MOVE7",green_check=1)
    
    #アブソル入れ替え処理後で実施
    #敗北チェックがめんどくさいので最悪何もせず負けた方がよい？
    def _2_story_absol_move7(self):
        return self.story_Template_battle_function(bkprg_ret="2_STORY_ABSOL_MOVE6",prg_ret="2_STORY_ABSOL_MOVE8",noprg_ret="2_STORY_ABSOL_MOVE7",Xaction=1,Aaction=1,Yaction=0,Baction=1,lockon_endskip=0,get_chanceicon4=0,noCp=1,battle_mode=1)

        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE"):# or self.image_check("TEXT_WHITE_COMMENT"):
            self.battle_coCp_noloop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        #elif self.image_check("TEXT_BLACK_COMMENT"):
        #    self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
        #    for i in range(10):
        #        self.wait(1.0)
        #        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
        #            self.press(Direction(Stick.LEFT,75), duration=4.0, wait=0.5)
        #            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
        #            return "2_STORY_W_LANK_MOVE3"
        #        elif self.image_check("TEXT_BLACK_COMMENT"):
        #            return "2_STORY_W_LANK_MOVE3"
        #elif self.image_check("EVENT_MARKER_CENTER_WIDE"):
        #    self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
        #    return "2_STORY_W_LANK_MOVE3"
        elif self.image_check("TEXT_WHITE_COMMENT"):
            return "2_STORY_ABSOL_MOVE8"
        elif self.image_check("COIN_ICON"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_ABSOL_MOVE8"
        return "2_STORY_ABSOL_MOVE7"
    
    
    
    def _2_story_absol_move8(self):
        return self.story_Template_battle_after(bkprg_ret="2_STORY_ABSOL_MOVE7",prg_ret="2_STORY_ABSOL_MOVE9")

        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="BATTLE_BALL_CHECK",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                self.wait(1.0)
                if not (self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE")):
                    return "2_STORY_MAPPING_110"#
                else:
                    return "2_STORY_ABSOL_MOVE7"

        return "2_STORY_ABSOL_MOVE8"
    
    #Wゾーン8-10のマッピング
    def _2_story_mapping_110(self):
        ### AUTO_SAVE_POINT
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "2_STORY_MAPPING_111"
        else:
            return "2_STORY_MAPPING_110"

    def _2_story_mapping_111(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(2,0,-3)#ポケセンターメディオに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_112"
        else:
            return "2_STORY_MAPPING_111"
    
    def _2_story_mapping_112(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,330), duration=3.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,50), duration=16.7, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,110), duration=24.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,80), duration=2.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_113"
        return "2_STORY_MAPPING_112"
    
    def _2_story_mapping_113(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_W_ZONE8"):
                print("MOVEPOINT_TARGET_W_ZONE8")
            if self.image_check("MOVEPOINT_PIC_W_ZONE8"):
                print("MOVEPOINT_PIC_W_ZONE8")
            
        else:
            ret = self.Common_goto(4,0,-1,movepoint_check=1)#Wゾーン8が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_W_ZONE8",pic2="MOVEPOINT_PIC_W_ZONE8") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_114_0"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_110"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_113"
            else:
                return "2_STORY_MAPPING_113"
        return "2_STORY_MAPPING_113"
    
    def _2_story_mapping_114_0(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "2_STORY_MAPPING_114"
        else:
            return "2_STORY_MAPPING_114_0"
    
    def _2_story_mapping_114(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(3,1,2)#カフェスロラームに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_114_1"
        else:
            return "2_STORY_MAPPING_114"

    def _2_story_mapping_114_1(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=3.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,200), duration=3.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_115"
        return "2_STORY_MAPPING_114_1"
        
    def _2_story_mapping_115(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_W_ZONE9"):
                print("MOVEPOINT_TARGET_W_ZONE9")
            if self.image_check("MOVEPOINT_PIC_W_ZONE9"):
                print("MOVEPOINT_PIC_W_ZONE9")
            
        else:
            ret = self.Common_goto(4,0,-1,movepoint_check=1)#Wゾーン9が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_W_ZONE9",pic2="MOVEPOINT_PIC_W_ZONE9") == True:
                    self.Common_goto_jump()
                    return "2_STORY_MAPPING_116"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_114_0"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_115"
            else:
                return "2_STORY_MAPPING_115"
        return "2_STORY_MAPPING_115"

    def _2_story_mapping_116_0(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "2_STORY_MAPPING_116"
        else:
            return "2_STORY_MAPPING_116_0"
    
    def _2_story_mapping_116(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(3,0,6)#カフェフォーカスに移動で位置確定
        if ret == "START":
            return "2_STORY_MAPPING_116_1"
        else:
            return "2_STORY_MAPPING_116"
        
    def _2_story_mapping_116_1(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,350), duration=5.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,80), duration=10.5, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=4.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MAPPING_117"
        return "2_STORY_MAPPING_116_1"
        
    def _2_story_mapping_117(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_W_ZONE10"):
                print("MOVEPOINT_TARGET_W_ZONE10")
            if self.image_check("MOVEPOINT_PIC_W_ZONE10"):
                print("MOVEPOINT_PIC_W_ZONE10")
            
        else:
            ret = self.Common_goto(4,0,-1,movepoint_check=1)#Wゾーン10が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_W_ZONE10",pic2="MOVEPOINT_PIC_W_ZONE10") == True:
                    self.Common_goto_jump()
                    return "2_STORY_ABSOL_MOVE9"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MAPPING_116_0"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "2_STORY_MAPPING_117"
            else:
                return "2_STORY_MAPPING_117"
        return "2_STORY_MAPPING_117"
    

    def _2_story_absol_move9(self):
        ret = self.Common_goto(1,0,-4)#レストランドリニューへ移動
        if ret == "START":
            return "2_STORY_ABSOL_MOVE10"
        else:
            return "2_STORY_ABSOL_MOVE9"
    
    def _2_story_absol_move10(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,230), duration=10.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,300), duration=4.0, wait=1.0)
            self.wait(0.5)
            return "2_STORY_ABSOL_MOVE11"
        return "2_STORY_ABSOL_MOVE10"
    
    def _2_story_absol_move11(self):
        return self.story_Template_battle_before(noprg_ret="2_STORY_ABSOL_MOVE11",prg_ret="2_STORY_ABSOL_MOVE12",green_check=1)
    
    def _2_story_absol_move12(self):
        return self.story_Template_battle_function(bkprg_ret="2_STORY_ABSOL_MOVE11",prg_ret="2_STORY_ABSOL_MOVE13",noprg_ret="2_STORY_ABSOL_MOVE12",Xaction=1,Aaction=1,Yaction=0,Baction=1,lockon_endskip=0,get_chanceicon4=0,noCp=1)
    
    def _2_story_absol_move13(self):
        return self.story_Template_battle_after(bkprg_ret="2_STORY_ABSOL_MOVE12",prg_ret="2_STORY_ABSOL_MOVE14")
    
    def _2_story_absol_move14(self):
        ### AUTO_SAVE_POINT
        self.battle_zone_loop_num = 1
        self.no_Cplus=1
        self.za_infi_main_current_state = self.STATE_ZA_INFI_MAIN_FUNCTION[self.za_infi_main_current_state]()
        self.wait(self.SLEEPLIST[9][2])
        if self.za_infi_main_current_state == "ZA_INFI_QUASAR_LOOP":
            self.za_infi_main_current_state = "ZA_INFI_MAIN_START"
            return "2_STORY_ABSOL_MOVE15"
        else: 
            return "2_STORY_ABSOL_MOVE14"
    
    def _2_story_absol_move15(self):
        ret = self.Common_goto(1,1,0)#クェーサー社へ移動
        if ret == "START":
            return "2_STORY_ABSOL_MOVE16"
        else:
            return "2_STORY_ABSOL_MOVE15"
    
    def _2_story_absol_move16(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,130), duration=12.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,58), duration=2.2, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_ABSOL_MOVE17"
        return "2_STORY_ABSOL_MOVE16"
    
    def _2_story_absol_move17(self):
        return self.story_Template_battle_before(noprg_ret="2_STORY_ABSOL_MOVE17",prg_ret="2_STORY_ABSOL_MOVE18",green_check=1)
    
    def _2_story_absol_move18(self):
        return self.story_Template_battle_function(bkprg_ret="2_STORY_ABSOL_MOVE17",prg_ret="2_STORY_ABSOL_MOVE19",noprg_ret="2_STORY_ABSOL_MOVE18",Xaction=1,Aaction=1,Yaction=0,Baction=1,lockon_endskip=0,get_chanceicon4=0,noCp=1)
    
    def _2_story_absol_move19(self):
        return self.story_Template_battle_after(bkprg_ret="2_STORY_ABSOL_MOVE18",prg_ret="2_STORY_ABSOL_MOVE20")
    
    def _2_story_absol_move20(self):
        ### AUTO_SAVE_POINT
        ret = self.Common_goto(1,1,0)#クェーサー社へ移動
        if ret == "START":
            return "2_STORY_ABSOL_MOVE21"
        else:
            return "2_STORY_ABSOL_MOVE20"
    
    def _2_story_absol_move21(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=8.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_ABSOL_MOVE22"
        return "2_STORY_ABSOL_MOVE21"
    
    def _2_story_absol_move22(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                self.wait(1.0)
                return "2_STORY_ABSOL_MOVE23"
        return "2_STORY_ABSOL_MOVE22"
    
    def _2_story_absol_move23(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,120), duration=4.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_ABSOL_MOVE24"
        return "2_STORY_ABSOL_MOVE23"
    
    def _2_story_absol_move24(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                self.wait(1.0)
                return "2_STORY_ABSOL_MOVE25"
        return "2_STORY_ABSOL_MOVE24"
    
    def _2_story_absol_move25(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,80), duration=5.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,130), duration=0.5, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_ABSOL_MOVE26"
        return "2_STORY_ABSOL_MOVE25"
    
    def _2_story_absol_move26(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                self.wait(1.0)
                return "2_STORY_ABSOL_MOVE27"
        return "2_STORY_ABSOL_MOVE26"
    
    def _2_story_absol_move27(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,270), duration=15.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,230), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_ABSOL_MOVE28"
        return "2_STORY_ABSOL_MOVE27"
    
    def _2_story_absol_move28(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                self.wait(1.0)
                return "2_STORY_ABSOL_MOVE29"
        return "2_STORY_ABSOL_MOVE28"
    
    def _2_story_absol_move29(self):
        ret = self.Common_goto(3,0,3)#ヌーヴォカフェへ移動
        if ret == "START":
            return "2_STORY_ABSOL_MOVE30"
        else:
            return "2_STORY_ABSOL_MOVE29"
    
    def _2_story_absol_move30(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.wait(0.5)
            return "2_STORY_ABSOL_MOVE31"
        return "2_STORY_ABSOL_MOVE30"
    
    def _2_story_absol_move31(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                self.wait(1.0)
                return "2_STORY_ABSOL_MOVE32"
        return "2_STORY_ABSOL_MOVE31"
    
    def _2_story_absol_move32(self):
        ret = self.Common_goto(1,0,3)#ホテルZへ移動
        if ret == "START":
            return "2_STORY_ABSOL_MOVE33"
        else:
            return "2_STORY_ABSOL_MOVE32"
    
    def _2_story_absol_move33(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_ABSOL_MOVE34"
        return "2_STORY_ABSOL_MOVE33"
    
    def _2_story_absol_move34(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,50), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,270), duration=0.7, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_ABSOL_MOVE35"
        return "2_STORY_ABSOL_MOVE34"
    
    def _2_story_absol_move35(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                self.wait(1.0)
                return "2_STORY_ABSOL_MOVE36"
        return "2_STORY_ABSOL_MOVE35"
    
    def _2_story_absol_move36(self):
        ret = self.Common_goto(1,0,5)#レストランフツーへ移動
        if ret == "START":
            return "2_STORY_ABSOL_MOVE37"
        else:
            return "2_STORY_ABSOL_MOVE36"
    
    def _2_story_absol_move37(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_ABSOL_MOVE38"
        return "2_STORY_ABSOL_MOVE37"
    
    def _2_story_absol_move38(self):
        if self.image_check("WANINOKO_ICON"):
            self.press(Direction(Stick.LEFT,30), duration=0.1, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_RESTAURANT_DOHUTSU_LOOP"
        return "2_STORY_ABSOL_MOVE38"
    
    def _2_story_restaurant_dohutsu_loop(self):
        if self.image_check("ESCAPE"):
            self._2_story_restaurant_dohutsu_black_check=0
            self._2_story_restaurant_dohutsu_white_check=1
            self.battle_coCp_noloop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self._2_story_restaurant_dohutsu_white_check=0
            self._2_story_restaurant_dohutsu_black_check+=1
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
        else:
            if self.image_check("TEXT_WHITE_COMMENT"):
                #self.wait(0.3)
                self._2_story_restaurant_dohutsu_white_check=1
                if (self._2_story_restaurant_dohutsu_black_check >= 3):
                    self._2_story_restaurant_dohutsu_battle_count+=1
                    if self._2_story_restaurant_dohutsu_battle_count >= self._2_story_restaurant_dohutsu_loop_threshold:
                        self.pressRep(Button.B, repeat=20, duration=0.15, wait=0.5, interval=0.1)
                        return "2_STORY_MEGA_MOVE1"
                else:
                    self._2_story_restaurant_dohutsu_black_check=0
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1) 
                    
                self._2_story_restaurant_dohutsu_black_check=0
                
            else:
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
        return "2_STORY_RESTAURANT_DOHUTSU_LOOP"
    
    
    ###進化と技設定
    
    def _2_story_mega_move1(self):
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "2_STORY_MEGA_MOVE2"
        else:
            return "2_STORY_MEGA_MOVE1"
    
    def _2_story_mega_move2(self):
        ret = self.Common_goto(3,1,0)#ヌーヴォカフェ２号へ移動
        if ret == "START":
            return "2_STORY_MEGA_MOVE3"
        else:
            return "2_STORY_MEGA_MOVE2"
    
    def _2_story_mega_move3(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,190), duration=20.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,200), duration=15.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,325), duration=11.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,330), duration=6.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,60), duration=6.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,0), duration=10.0, wait=1.0)
            self.wait(0.5)
            return "2_STORY_MEGA_MOVE4"
        return "2_STORY_MEGA_MOVE3"
    
    def _2_story_mega_move4(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_MEGA_MOVE5"
        return "2_STORY_MEGA_MOVE4"
    
    def _2_story_mega_move5(self):
        if self.mega_evolution_battle_mode_select(mode=0):
            return "2_STORY_MEGA_MOVE6" 
        return "2_STORY_MEGA_MOVE5"
    
    def _2_story_mega_move6(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_MEGA_MOVE7"
        return "2_STORY_MEGA_MOVE6"
    
    def _2_story_mega_move7(self):
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "2_STORY_MEGA_MOVE8"
        else:
            return "2_STORY_MEGA_MOVE7"
    
    def _2_story_mega_move8(self):
        ret = self.Common_goto(1,0,-2)#レストランキワミへ移動
        if ret == "START":
            return "2_STORY_MEGA_MOVE9"
        else:
            return "2_STORY_MEGA_MOVE8"
    
    def _2_story_mega_move9(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,300), duration=15.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,180), duration=6.0, wait=1.0)
            self.wait(0.5)
            return "2_STORY_MEGA_MOVE10"
        return "2_STORY_MEGA_MOVE9"
    
    def _2_story_mega_move10(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="BATTLE_BALL_CHECK",endpicture2="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_MEGA_MOVE11" 
        return "2_STORY_MEGA_MOVE10"
    
    def _2_story_mega_move11(self):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE"):# or self.image_check("TEXT_WHITE_COMMENT"):
            self.battle_Cp_loop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            for i in range(10):
                self.wait(1.0)
                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                    self.press(Direction(Stick.LEFT,90), duration=0.3, wait=0.5)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MEGA_MOVE10"
                elif self.image_check("TEXT_BLACK_COMMENT"):
                    return "2_STORY_MEGA_MOVE10"
        elif self.image_check("EVENT_MARKER_CENTER_WIDE") or self.image_check("EVENT_MARKER_RIGHT_WIDE"):
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MEGA_MOVE10"
        elif self.image_check("TEXT_WHITE_COMMENT"):
            return "2_STORY_MEGA_MOVE12"
        elif self.image_check("COIN_ICON"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
        return "2_STORY_MEGA_MOVE11"
    
    def _2_story_mega_move12(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_MEGA_MOVE13" 
        return "2_STORY_MEGA_MOVE12"
    
    def _2_story_mega_move13(self):
        ###AUTO SAVE アスレチックのため、ミスがあった場合はセーブポイントから開始とする。
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,88), duration=8.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=6.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,270), duration=0.3, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,180), duration=0.4, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,300), duration=0.5, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=5, duration=0.15, wait=0.5, interval=0.1)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=8.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,170), duration=0.5, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=8.0, wait=1.0)
            self.wait(0.5)
            return "2_STORY_MEGA_MOVE14"
        return "2_STORY_MEGA_MOVE13"
    
    def _2_story_mega_move14(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_MEGA_MOVE15"
        return "2_STORY_MEGA_MOVE14"
    
    def _2_story_mega_move15(self):
        if self.mega_evolution_battle_mode_select(mode=0):
            return "2_STORY_MEGA_MOVE16" 
        return "2_STORY_MEGA_MOVE15"
    
    def _2_story_mega_move16(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_MEGA_MOVE17"
        return "2_STORY_MEGA_MOVE16"
    
    def _2_story_mega_move17(self):
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "2_STORY_MEGA_MOVE18"
        else:
            return "2_STORY_MEGA_MOVE17"
    
    def _2_story_mega_move18(self):
        ret = self.Common_goto(1,1,0)#クェーサー社へ移動
        if ret == "START":
            return "2_STORY_MEGA_MOVE19"
        else:
            return "2_STORY_MEGA_MOVE18"
    
    def _2_story_mega_move19(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,270), duration=1.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,355), duration=24.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,100), duration=13.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,180), duration=5.0, wait=1.0)
            self.wait(0.5)
            return "2_STORY_MEGA_MOVE20"
        return "2_STORY_MEGA_MOVE19"
    
    def _2_story_mega_move20(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="BATTLE_BALL_CHECK",endpicture2="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_MEGA_MOVE21" 
        return "2_STORY_MEGA_MOVE20"
    
    def _2_story_mega_move21(self):
        if self.mega_evolution_battle_mode_select(mode=0):
            return "2_STORY_MEGA_MOVE22" 
        return "2_STORY_MEGA_MOVE21"
    
    def _2_story_mega_move22(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_MEGA_MOVE23" 
        return "2_STORY_MEGA_MOVE22"
    
    def _2_story_mega_move23(self):
        if self.check_picture==1:
            if self.image_check("ZA_ROYALE"):
                print("ZA_ROYALE")
                
        else:
            ret = self.Common_goto(1,0,3)#ホテルZへ移動
            if ret == "START":
                return "2_STORY_MEGA_MOVE24"
            else:
                return "2_STORY_MEGA_MOVE23"
        return "2_STORY_MEGA_MOVE23"
    
    def _2_story_mega_move24(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.wait(0.5)
            return "2_STORY_MEGA_MOVE25"
        return "2_STORY_MEGA_MOVE24"
    
    def _2_story_mega_move25(self):
        if self.image_check("TEXT_WHITE_COMMENT") or self.image_check("TEXT_BLACK_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",endpicture3="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_MEGA_MOVE26" 

        return "2_STORY_MEGA_MOVE25"
    
    def _2_story_mega_move26(self):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE"):# or self.image_check("TEXT_WHITE_COMMENT"):
            self.battle_Cp_loop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            for i in range(10):
                self.wait(1.0)
                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                    self.press(Direction(Stick.LEFT,90), duration=3.0, wait=0.5)
                    #self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    return "2_STORY_MEGA_MOVE25"
                elif self.image_check("TEXT_BLACK_COMMENT"):
                    return "2_STORY_MEGA_MOVE25"
        elif self.image_check("EVENT_MARKER_CENTER_WIDE") or self.image_check("EVENT_MARKER_RIGHT_WIDE"):
            self.press(Direction(Stick.LEFT,90), duration=3.0, wait=0.5)
            #self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "2_STORY_MEGA_MOVE25"
        elif self.image_check("TEXT_WHITE_COMMENT"):
            return "2_STORY_MEGA_MOVE27"
        #elif self.image_check("COIN_ICON"):
        #    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
        return "2_STORY_MEGA_MOVE26"
    
    def _2_story_mega_move27(self):
        if self.image_check("TEXT_WHITE_COMMENT") or self.image_check("TEXT_BLACK_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",endpicture3="ESCAPE",not_endpicture="ZA_ROYALE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "2_STORY_END"
        return "2_STORY_MEGA_MOVE27"
    
    def _2_story_end(self):
        return "2_STORY_START_CHECK" 
    

    ######################################################
    # MAIN_3_F_LANK SUB FUNCTION
    ######################################################
    def _3_story_start_check(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            return "3_STORY_CANARI_1"
        return "3_STORY_START_CHECK"

    def _3_story_canari_1(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_2"
        return "3_STORY_CANARI_1"

    def _3_story_canari_2(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_3"

        return "3_STORY_CANARI_2"

    def _3_story_canari_3(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="BATTLE_BALL_CHECK",endpicture2="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "3_STORY_CANARI_4"
        return "3_STORY_CANARI_3"

    def _3_story_canari_4(self):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE"):# or self.image_check("TEXT_WHITE_COMMENT"):
            self.battle_Cp_loop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            for i in range(10):
                self.wait(1.0)
                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                    self.press(Direction(Stick.LEFT,90), duration=0.3, wait=0.5)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    return"3_STORY_CANARI_4"
                elif self.image_check("TEXT_BLACK_COMMENT"):
                    return "3_STORY_CANARI_4"
        elif self.image_check("EVENT_MARKER_CENTER_WIDE") or self.image_check("EVENT_MARKER_RIGHT_WIDE"):
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_4"
        #elif self.image_check("TEXT_WHITE_COMMENT"):
        #    return "3_STORY_CANARI_5"
        elif self.image_check("COIN_ICON"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_5"
        return "3_STORY_CANARI_4"

    def _3_story_canari_5(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="BATTLE_BALL_CHECK",endpicture3="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                for i in range(10):
                    self.wait(0.5)
                    if (self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE")):
                        return "3_STORY_CANARI_4"
                return "3_STORY_CANARI_6"
        elif (self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE")):
            return "3_STORY_CANARI_4"

        return "3_STORY_CANARI_5"

    def _3_story_canari_6(self):
        ### AUTO_SAVE_POINT
        self.battle_zone_loop_num = 1
        self.no_Cplus=1
        self.za_infi_main_current_state = self.STATE_ZA_INFI_MAIN_FUNCTION[self.za_infi_main_current_state]()
        self.wait(self.SLEEPLIST[9][2])
        if self.za_infi_main_current_state == "ZA_INFI_QUASAR_LOOP":
            self.za_infi_main_current_state = "ZA_INFI_MAIN_START"
            return "3_STORY_CANARI_7"
        else: 
            return "3_STORY_CANARI_6"

    def _3_story_canari_7(self):
        ret = self.Common_goto(1,0,3)#ホテルZへ移動
        if ret == "START":
            return "3_STORY_CANARI_8"
        else:
            return "3_STORY_CANARI_7"

    def _3_story_canari_8(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_9"
        return "3_STORY_CANARI_8"

    def _3_story_canari_9(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,50), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,270), duration=0.5, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_10"
        return "3_STORY_CANARI_9"

    def _3_story_canari_10(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "3_STORY_END" 

        return "3_STORY_CANARI_10"
    
    def _3_story_canari_11(self):
        ret = self.Common_change_time_set(check_timing="NIGHT")#想定外に時間変更があると補足できないため
        if ret == "START":
            return "3_STORY_CANARI_12"
        else:
            return "3_STORY_CANARI_11"
    
    def _3_story_canari_12(self):
        ret = self.Common_goto(2,0,3)#ポケセンターローズへ移動
        if ret == "START":
            return "3_STORY_CANARI_13"
        else:
            return "3_STORY_CANARI_12"
    
    def _3_story_canari_13(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,0), duration=9.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=13.0, wait=1.0)
            self.wait(0.5)

            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "3_STORY_CANARI_14"
        return "3_STORY_CANARI_13"
    
    def _3_story_canari_14(self):
        for i in range(10):
            if self.image_check("TEXT_WHITE_COMMENT"):
                if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                    return "3_STORY_CANARI_15"
            self.wait(0.5)
        if not self.image_check("TEXT_WHITE_COMMENT"):
            return "3_STORY_CANARI_11"
        return "3_STORY_CANARI_14"
    
    def _3_story_canari_15(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,100), duration=10.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,80), duration=1.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,180), duration=0.3, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "3_STORY_CANARI_16"
        return "3_STORY_CANARI_15"
    
    def _3_story_canari_16(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="3_SELECT",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sleeptime=0.5):
                self.wait(0.5)
                return "3_STORY_CANARI_17"
        return "3_STORY_CANARI_16"
    
    def _3_story_canari_17(self):
        if self.image_check("3_SELECT"):
            for i in range(2):
                self.etc_sendCommand("Lbutton_down")
                self.wait(0.3)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_18"
            
        return "3_STORY_CANARI_17"
    
    def _3_story_canari_18(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="3_SELECT",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sleeptime=0.5):
                self.wait(0.5)
                return "3_STORY_CANARI_19"
        return "3_STORY_CANARI_18"
    
    def _3_story_canari_19(self):
        if self.image_check("3_SELECT"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_20"
        return "3_STORY_CANARI_19"
    
    def _3_story_canari_20(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="3_SELECT",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sleeptime=0.5):
                self.wait(0.5)
                return "3_STORY_CANARI_21"
        return "3_STORY_CANARI_20"
    
    def _3_story_canari_21(self):
        if self.image_check("3_SELECT"):
            self.etc_sendCommand("Lbutton_down")
            self.wait(0.3)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_22"
        return "3_STORY_CANARI_21"
    
    def _3_story_canari_22(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            return "3_STORY_CANARI_23"

        return "3_STORY_CANARI_22"
    
    def _3_story_canari_23(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,190), duration=2.0, wait=1.0)
            self.wait(0.5)

            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "3_STORY_CANARI_24"
        return "3_STORY_CANARI_23"
    
    def _3_story_canari_24(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            return "3_STORY_CANARI_25"

        return "3_STORY_CANARI_24"
    
    def _3_story_canari_25(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,350), duration=2.0, wait=1.0)
            self.wait(0.5)

            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "3_STORY_CANARI_26"
        return "3_STORY_CANARI_25"
    
    def _3_story_canari_26(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            return "3_STORY_CANARI_27"

        return "3_STORY_CANARI_26"
    
    def _3_story_canari_27(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,190), duration=2.0, wait=1.0)
            self.wait(0.5)

            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "3_STORY_CANARI_28"
        return "3_STORY_CANARI_27"
    
    def _3_story_canari_28(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            return "3_STORY_CANARI_29"
        return "3_STORY_CANARI_28"
    
    def _3_story_canari_29(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=4.0, wait=1.0)
            self.wait(0.5)
            return "3_STORY_CANARI_30"
        return "3_STORY_CANARI_29"
    
    def _3_story_canari_30(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            return "3_STORY_CANARI_31"
        return "3_STORY_CANARI_30"
    
    def _3_story_canari_31(self):
        ret = self.Common_goto(3,2,0)#カフェおとこまえへ移動
        if ret == "START":
            return "3_STORY_CANARI_32"
        else:
            return "3_STORY_CANARI_31"
    
    def _3_story_canari_32(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            return "3_STORY_CANARI_33"
        return "3_STORY_CANARI_32"
    
    def _3_story_canari_33(self):
        ret = self.Common_change_time_set(check_timing="NIGHT")#想定外に時間変更があると補足できないため
        if ret == "START":
            return "3_STORY_CANARI_34"
        else:
            return "3_STORY_CANARI_33"
    
    def _3_story_canari_34(self):
        ret = self.Common_goto(2,0,3)#ポケセンターローズへ移動
        if ret == "START":
            return "3_STORY_CANARI_35"
        else:
            return "3_STORY_CANARI_34"
    
    def _3_story_canari_35(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,0), duration=9.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=8.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,0), duration=15.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=2.3, wait=1.0)
            self.wait(0.5)
            return "3_STORY_CANARI_36"
        return "3_STORY_CANARI_35"
    
    def _3_story_canari_36(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="BATTLE_BALL_CHECK",endpicture3="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            return "3_STORY_CANARI_37"
        return "3_STORY_CANARI_36"
    
    def _3_story_canari_37(self):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE"):# or self.image_check("TEXT_WHITE_COMMENT"):
            self.battle_Cp_loop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            for i in range(10):
                self.wait(1.0)
                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                    self.press(Direction(Stick.LEFT,75), duration=0.3, wait=0.5)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    return"3_STORY_CANARI_36"
                elif self.image_check("TEXT_BLACK_COMMENT"):
                    return "3_STORY_CANARI_36"
        elif self.image_check("EVENT_MARKER_CENTER_WIDE") or self.image_check("EVENT_MARKER_RIGHT_WIDE"):
            self.press(Direction(Stick.LEFT,75), duration=0.3, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_36"
        elif self.image_check("TEXT_WHITE_COMMENT"):
            return "3_STORY_CANARI_38"
        elif self.image_check("COIN_ICON"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_38"

        return "3_STORY_CANARI_37"
    
    def _3_story_canari_38(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="BATTLE_BALL_CHECK",endpicture3="ESCAPE",endpicture4="4_SELECT",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            for i in range(10):
                self.wait(0.5)
                if (self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE")):
                    return "3_STORY_CANARI_37"
                elif self.image_check("4_SELECT"):
                    self.wait(1.0)
                    return "3_STORY_CANARI_39"
            return "3_STORY_CANARI_38"
        elif (self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE")):
            return "3_STORY_CANARI_37"

        return "3_STORY_CANARI_38"
    
    def _3_story_canari_39(self):
        if self.image_check("4_SELECT"):
            for i in range(3):
                self.etc_sendCommand("Lbutton_down")
                self.wait(0.3)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_40"
        return "3_STORY_CANARI_39"
    
    def _3_story_canari_40(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            return "3_STORY_CANARI_41"
        return "3_STORY_CANARI_40"
    
    def _3_story_canari_41(self):
        ret = self.Common_goto(1,0,4)#ラシーヌ工務店へ移動
        if ret == "START":
            return "3_STORY_CANARI_42"
        else:
            return "3_STORY_CANARI_41"
    
    def _3_story_canari_42(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_43"
        return "3_STORY_CANARI_42"
    
    def _3_story_canari_43(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_44"
        return "3_STORY_CANARI_43"
    
    def _3_story_canari_44(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",endpicture3="BATTLE_BALL_CHECK",endpicture4="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            return "3_STORY_CANARI_45"
        return "3_STORY_CANARI_44"
    
    def _3_story_canari_45(self):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE"):# or self.image_check("TEXT_WHITE_COMMENT"):
            self.battle_Cp_loop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            for i in range(10):
                self.wait(1.0)
                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                    self.press(Direction(Stick.LEFT,75), duration=0.3, wait=0.5)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    return"3_STORY_CANARI_44"
                elif self.image_check("TEXT_BLACK_COMMENT"):
                    return "3_STORY_CANARI_44"
        elif self.image_check("EVENT_MARKER_CENTER_WIDE") or self.image_check("EVENT_MARKER_RIGHT_WIDE"):
            self.press(Direction(Stick.LEFT,75), duration=0.3, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_44"
        elif self.image_check("TEXT_WHITE_COMMENT"):
            return "3_STORY_CANARI_46"
        elif self.image_check("COIN_ICON"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_46"
        return "3_STORY_CANARI_45"
    
    def _3_story_canari_46(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="BATTLE_BALL_CHECK",endpicture3="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            for i in range(10):
                self.wait(0.5)
                if (self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE")):
                    return "3_STORY_CANARI_45"
            return "3_STORY_CANARI_47"
        elif (self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE")):
            return "3_STORY_CANARI_45"
        return "3_STORY_CANARI_46"
    
    def _3_story_canari_47(self):
        #AUTOSAVE
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,130), duration=10.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,70), duration=3.0, wait=1.0)
            self.wait(0.5)
            #self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_48"
        return "3_STORY_CANARI_47"
    
    def _3_story_canari_48(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",endpicture3="BATTLE_BALL_CHECK",endpicture4="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            return "3_STORY_CANARI_49"
        return "3_STORY_CANARI_48"
    
    def _3_story_canari_49(self):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE"):# or self.image_check("TEXT_WHITE_COMMENT"):
            self.battle_Cp_loop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            for i in range(10):
                self.wait(1.0)
                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                    self.press(Direction(Stick.LEFT,90), duration=0.3, wait=0.5)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    return"3_STORY_CANARI_48"
                elif self.image_check("TEXT_BLACK_COMMENT"):
                    return "3_STORY_CANARI_48"
        elif self.image_check("EVENT_MARKER_CENTER_WIDE") or self.image_check("EVENT_MARKER_LEFT_WIDE"):
            self.press(Direction(Stick.LEFT,90), duration=0.3, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_48"
        elif self.image_check("TEXT_WHITE_COMMENT"):
            return "3_STORY_CANARI_50"
        elif self.image_check("COIN_ICON"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_CANARI_50"
        return "3_STORY_CANARI_49"
    
    def _3_story_canari_50(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="BATTLE_BALL_CHECK",endpicture3="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            for i in range(10):
                self.wait(0.5)
                if (self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE")):
                    return "3_STORY_CANARI_49"
            return "3_STORY_MEGA_MOVE1"
        elif (self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE")):
            return "3_STORY_CANARI_49"
        return "3_STORY_CANARI_50"
    
    def _3_story_mega_move1(self):
        #AUTOSAVE
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,30), duration=0.5, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_MEGA_MOVE2"
        return "3_STORY_MEGA_MOVE1"
    
    def _3_story_mega_move2(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "3_STORY_MEGA_MOVE3"
        return "3_STORY_MEGA_MOVE2"
    
    #Wゾーンマッピング 11-13   

    def _3_story_mega_move3(self):
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "3_STORY_MEGA_MOVE4"
        else:
            return "3_STORY_MEGA_MOVE3"
    
    def _3_story_mega_move4(self):
        ret = self.Common_goto(1,0,3)#ホテルZへ移動
        if ret == "START":
            return "3_STORY_MEGA_MOVE5"
        else:
            return "3_STORY_MEGA_MOVE4"

    
    def _3_story_mega_move5(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,30), duration=3.5, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=15.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,120), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_MEGA_MOVE6"
        return "3_STORY_MEGA_MOVE5"
    
    def _3_story_mega_move6(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "3_STORY_MEGA_MOVE7"
        return "3_STORY_MEGA_MOVE6"
    
    def _3_story_mega_move7(self):
        #AUTOSAVE ロトムグライド開放
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.ROTOM_GLIDE(dir=90,a_count=20)
            return "3_STORY_MEGA_MOVE8"
        return "3_STORY_MEGA_MOVE7"
    
    def _3_story_mega_move8(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "3_STORY_MEGA_MOVE9"
        return "3_STORY_MEGA_MOVE8"
    
    def _3_story_mega_move9(self):
        #AUTOSAVE
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,180), duration=2.0, wait=1.0)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=2.0, wait=1.0)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,180), duration=3.8, wait=1.0)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,170), duration=1.0, wait=1.0)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,170), duration=0.4, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,75), duration=12.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,50), duration=2.0, wait=1.0)
            self.wait(0.5) 
            self.press(Direction(Stick.LEFT,320), duration=3.0, wait=1.0)
            self.wait(0.5) 
            self.press(Direction(Stick.LEFT,310), duration=4.0, wait=1.0)
            self.wait(0.5) 
            return "3_STORY_MEGA_MOVE10"
        return "3_STORY_MEGA_MOVE9"
    
    def _3_story_mega_move10(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "3_STORY_MEGA_MOVE11"
        return "3_STORY_MEGA_MOVE10"
    
    def _3_story_mega_move11(self):
        if self.mega_evolution_battle_mode_select(mode=0):
            return "3_STORY_MEGA_MOVE12"
        return "3_STORY_MEGA_MOVE11"
    
    def _3_story_mega_move12(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.5):
                return "3_STORY_MEGA_MOVE13"
        return "3_STORY_MEGA_MOVE12"
    
    def _3_story_mega_move13(self):
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "3_STORY_MEGA_MOVE14"
        else:
            return "3_STORY_MEGA_MOVE13"
    
    def _3_story_mega_move14(self):
        ret = self.Common_goto(2,0,-2)#ポケセンタージョーヌへ移動
        if ret == "START":
            return "3_STORY_MEGA_MOVE15"
        else:
            return "3_STORY_MEGA_MOVE14"
    
    def _3_story_mega_move15(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,330), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,240), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,150), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,100), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,210), duration=4.2, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,180), duration=14.5, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,270), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,240), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,330), duration=5.0, wait=1.0)
            self.wait(0.5)
            return "3_STORY_MEGA_MOVE16"
        return "3_STORY_MEGA_MOVE15"
    
    def _3_story_mega_move16(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "3_STORY_MEGA_MOVE17"
        return "3_STORY_MEGA_MOVE16"
    
    def _3_story_mega_move17(self):
        if self.mega_evolution_battle_mode_select(mode=0):
            return "3_STORY_MEGA_MOVE18"

        return "3_STORY_MEGA_MOVE17"
    
    def _3_story_mega_move18(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.5):
                return "3_STORY_MEGA_MOVE19"

        return "3_STORY_MEGA_MOVE18"
    
    def _3_story_mega_move19(self):
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "3_STORY_MEGA_MOVE20"
        else:
            return "3_STORY_MEGA_MOVE19"
    
    def _3_story_mega_move20(self):
        ret = self.Common_goto(3,2,0)#カフェおとこまえへ移動
        if ret == "START":
            return "3_STORY_MEGA_MOVE21"
        else:
            return "3_STORY_MEGA_MOVE20"
    
    def _3_story_mega_move21(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,170), duration=8.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_MEGA_MOVE22"
        return "3_STORY_MEGA_MOVE21"
    
    def _3_story_mega_move22(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=1.6, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,180), duration=19.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,0), duration=1.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=0.7, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0)
            return "3_STORY_MEGA_MOVE23"
        return "3_STORY_MEGA_MOVE22"
    
    def _3_story_mega_move23(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.5):
                return "3_STORY_MEGA_MOVE24"
        return "3_STORY_MEGA_MOVE23"
    
    def _3_story_mega_move24(self):
        #AUTOSAVE
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,87), duration=7.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,0), duration=4.7, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=5.5, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,0), duration=1.5, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,93), duration=8.3, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,135), duration=2.0, wait=1.0)
            self.wait(0.5)
            return "3_STORY_MEGA_MOVE25"
        return "3_STORY_MEGA_MOVE24"
    
    def _3_story_mega_move25(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",endpicture3="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.5):
                return "3_STORY_MEGA_MOVE26"
        return "3_STORY_MEGA_MOVE25"
    
    def _3_story_mega_move26(self):
        if self.mega_evolution_battle_mode_select(mode=0):
            return "3_STORY_MEGA_MOVE27"
        return "3_STORY_MEGA_MOVE26"
        
    
    def _3_story_mega_move27(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.5):
                return "3_STORY_MEGA_MOVE28"
        return "3_STORY_MEGA_MOVE27"
    
    def _3_story_mega_move28(self):
        ret = self.Common_goto(1,0,3)#ホテルZへ移動
        if ret == "START":
            return "3_STORY_MEGA_MOVE29"
        else:
            return "3_STORY_MEGA_MOVE28"
    
    def _3_story_mega_move29(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "3_STORY_MEGA_MOVE30"
        return "3_STORY_MEGA_MOVE29"
    
    def _3_story_mega_move30(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.5):
                return "3_STORY_END"
        return "3_STORY_MEGA_MOVE30"
    
    def _3_story_end(self):
        return "3_STORY_START_CHECK" 

    ######################################################
    # MAIN_4_E_LANK SUB FUNCTION
    ######################################################
    def _4_story_start_check(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            return "4_STORY_SHIRO_1"
        return "4_STORY_START_CHECK"
    
    def _4_story_shiro_1(self):
        self.battle_zone_loop_num = 1
        self.no_Cplus=1
        self.za_infi_main_current_state = self.STATE_ZA_INFI_MAIN_FUNCTION[self.za_infi_main_current_state]()
        self.wait(self.SLEEPLIST[9][2])
        if self.za_infi_main_current_state == "ZA_INFI_QUASAR_LOOP":
            self.za_infi_main_current_state = "ZA_INFI_MAIN_START"
            return "4_STORY_SHIRO_2"
        else: 
            return "4_STORY_SHIRO_1"
    
    def _4_story_shiro_2(self):
        ### AUTO_SAVE_POINT
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "4_STORY_SHIRO_3"
        else:
            return "4_STORY_SHIRO_2"
    
    def _4_story_shiro_3(self):
        ### AUTO_SAVE_POINT
        ret = self.Common_goto(1,0,-1)#ジャスティス道場へ移動
        if ret == "START":
            return "4_STORY_SHIRO_4"
        else:
            return "4_STORY_SHIRO_3"

    
    def _4_story_shiro_4(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=7.0, wait=1.0)
            self.wait(0.5)
            #self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "4_STORY_SHIRO_5"
        return "4_STORY_SHIRO_4"
            
    def _4_story_shiro_5(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",endpicture3="BATTLE_BALL_CHECK",endpicture4="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "4_STORY_SHIRO_6"
        return "4_STORY_SHIRO_5"
    
    def _4_story_shiro_6(self):
        if self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE"):# or self.image_check("TEXT_WHITE_COMMENT"):
            self.battle_Cp_loop(Xaction=1,Aaction=1,Yaction=0,Baction=1)
        elif self.image_check("TEXT_BLACK_COMMENT"):
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.5, interval=0.1)
            for i in range(10):
                self.wait(1.0)
                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                    self.press(Direction(Stick.LEFT,90), duration=0.3, wait=0.5)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    return "4_STORY_SHIRO_5"
                elif self.image_check("TEXT_BLACK_COMMENT"):
                    return "4_STORY_SHIRO_5"
        elif self.image_check("EVENT_MARKER_CENTER_WIDE") or self.image_check("EVENT_MARKER_LEFT_WIDE"):
            self.press(Direction(Stick.LEFT,90), duration=0.3, wait=0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "4_STORY_SHIRO_5"
        elif self.image_check("TEXT_WHITE_COMMENT"):
            return "4_STORY_SHIRO_7"
        elif self.image_check("COIN_ICON"):
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "4_STORY_SHIRO_7"
        return "4_STORY_SHIRO_6"
    
    def _4_story_shiro_7(self):
        if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="BATTLE_BALL_CHECK",endpicture3="ESCAPE",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
            for i in range(5):
                self.wait(0.5)
                if (self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE")):
                    return "4_STORY_SHIRO6"
            return "4_STORY_SHIRO_7"
        elif (self.image_check("BATTLE_BALL_CHECK") or self.image_check("ESCAPE")):
            return "4_STORY_SHIRO_6"
        return "4_STORY_SHIRO_7"
    
    def _4_story_shiro_8(self):
        ret = self.Common_goto(2,0,1)#ポケセンメディオに移動で位置確定
        if ret == "START":
            return "4_STORY_SHIRO_9"
        else:
            return "4_STORY_SHIRO_8"
    
    def _4_story_shiro_9(self):
        ### AUTO_SAVE_POINT
        if self.Common_pokemon_recovery():
            return "4_STORY_SHIRO_10"
        else:
            return "4_STORY_SHIRO_9"
    
    def _4_story_shiro_10(self):
        ret = self.Common_goto(1,0,-6)#ハンサムハウスへ移動
        if ret == "START":
            return "4_STORY_SHIRO_11"
        else:
            return "4_STORY_SHIRO_10"
    
    def _4_story_shiro_11(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=0.5, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "4_STORY_SHIRO_12"
        return "4_STORY_SHIRO_11"
    
    def _4_story_shiro_12(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_13"
        return "4_STORY_SHIRO_12"
    
    def _4_story_shiro_13(self):
        ret = self.Common_goto(4,0,7)#Wゾーン8へ移動
        if ret == "START":
            return "4_STORY_SHIRO_14"
        else:
            return "4_STORY_SHIRO_13"
    
    def _4_story_shiro_14(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,270), duration=6.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,180), duration=8.0, wait=1.0)
            self.wait(0.5)
            return "4_STORY_SHIRO_15"
        return "4_STORY_SHIRO_14"
    
    def _4_story_shiro_15(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_16"
        return "4_STORY_SHIRO_15"
    
    def _4_story_shiro_16(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,120), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,180), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,120), duration=4.5, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "4_STORY_SHIRO_17"
        return "4_STORY_SHIRO_16"
    
    def _4_story_shiro_17(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_18"
        return "4_STORY_SHIRO_17"
    
    def _4_story_shiro_18(self):
        ret = self.Common_goto(3,0,3)#ヌーヴォカフェへ移動
        if ret == "START":
            return "4_STORY_SHIRO_19"
        else:
            return "4_STORY_SHIRO_18"
    
    def _4_story_shiro_19(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            return "4_STORY_SHIRO_20"
        return "4_STORY_SHIRO_19"
    
    def _4_story_shiro_20(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_21"
        return "4_STORY_SHIRO_20"
    
    def _4_story_shiro_21(self):
        ### AUTO_SAVE_POINT
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "4_STORY_SHIRO_21_1"
        else:
            return "4_STORY_SHIRO_21"
        
    def _4_story_shiro_21_1(self):
        ret = self.Common_goto(2,0,1)#ポケセンメディオに移動で位置確定
        if ret == "START":
            return "4_STORY_SHIRO_21_2"
        else:
            return "4_STORY_SHIRO_21_1"
    
    def _4_story_shiro_21_2(self):
        ### AUTO_SAVE_POINT
        if self.Common_pokemon_recovery():
            return "4_STORY_SHIRO_22"
        else:
            return "4_STORY_SHIRO_21_2"
    
    def _4_story_shiro_22(self):
        ### AUTO_SAVE_POINT
        ret = self.Common_goto(3,1,0)#ヌーヴォカフェ2号へ移動
        if ret == "START":
            return "4_STORY_SHIRO_23"
        else:
            return "4_STORY_SHIRO_22"
    
    def _4_story_shiro_23(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,200), duration=4.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,270), duration=10.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,320), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,270), duration=5.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,180), duration=5.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,110), duration=1.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,180), duration=0.1, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "4_STORY_SHIRO_24"
        return "4_STORY_SHIRO_23"
    
    def _4_story_shiro_24(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            if self.markerdir("EVENT"):
                return "4_STORY_SHIRO_25"
        return "4_STORY_SHIRO_24"
    
    def _4_story_shiro_25(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,120), duration=3.5, wait=1.0)
            return "4_STORY_SHIRO_26"
        return "4_STORY_SHIRO_25"
    
    def _4_story_shiro_26(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            if self.image_check("FIELD3"):
                self.etc_sendCommand("Lbutton_up")
                self.wait(1.0)
                return "4_STORY_SHIRO_27"
            elif self.image_check("FIELD_BACK3"):
                self.wait(1.0)
                return "4_STORY_SHIRO_27"
            else:
                self.etc_sendCommand("Lbutton_left")
                self.wait(1.0)

        return "4_STORY_SHIRO_26"
    
    def _4_story_shiro_27(self):
        self.wait(1.0)
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=0)
            if not self.image_check("EYE_CHECK_HIGH_POKE"):
                return "4_STORY_SHIRO_28"
        return "4_STORY_SHIRO_27"
    
    def _4_story_shiro_28(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            if self.markerdir("EVENT"):
                return "4_STORY_SHIRO_29"
        return "4_STORY_SHIRO_28"
    
    def _4_story_shiro_29(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "4_STORY_SHIRO_30"
        return "4_STORY_SHIRO_29"
    
    def _4_story_shiro_30(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(0.5)
            self.battle_coCp_noloop(Xaction=1,Aaction=1,Yaction=1,Baction=0)
            if not self.image_check("EYE_CHECK_HIGH_POKE"):
                return "4_STORY_SHIRO_31"
        return "4_STORY_SHIRO_30"
    
    def _4_story_shiro_31(self):
        if self.image_check("EYE_CHECK_HIGH_POKE"):
            return "4_STORY_SHIRO_30"
        ret = self.Common_goto(1,0,4)#ラシーヌ工務店へ移動
        if ret == "START":
            return "4_STORY_SHIRO_32"
        else:
            return "4_STORY_SHIRO_31"
    
    def _4_story_shiro_32(self):
        ret = self.common_skill_change_function(1,1,"X",1,targetskill_pic="REIBI_SKILL")
        #if self.common_skill_change_current_state
        if ret == "COMMON_SKILL_CHANGE_FALSE":
            self.common_skill_change_current_state="COMMON_SKILL_CHANGE_START"
            return "4_STORY_SHIRO_21"
        elif ret == "COMMON_SKILL_CHANGE_START":
            return "4_STORY_SHIRO_33"
        else: 
            return "4_STORY_SHIRO_32"
    
    def _4_story_shiro_33(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "4_STORY_SHIRO_34"
        return "4_STORY_SHIRO_33"

    def _4_story_shiro_34(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,30), duration=15.0, wait=1.0)
            self.wait(0.5)
            return "4_STORY_SHIRO_35"
        return "4_STORY_SHIRO_34"
    
    def _4_story_shiro_35(self):
        return self.story_Template_battle_before(noprg_ret="4_STORY_SHIRO_35",prg_ret="4_STORY_SHIRO_36",green_check=1)
    
    def _4_story_shiro_36(self):
        return self.story_Template_battle_function(bkprg_ret="4_STORY_SHIRO_35",prg_ret="4_STORY_SHIRO_37",noprg_ret="4_STORY_SHIRO_36")
    
    def _4_story_shiro_37(self):
        return self.story_Template_battle_after(bkprg_ret="4_STORY_SHIRO_36",prg_ret="4_STORY_SHIRO_38",selected_pic="4_SELECT",selected_target=1)
    
    def _4_story_shiro_38(self):
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "4_STORY_SHIRO_39"
        else:
            return "4_STORY_SHIRO_38"
    
    def _4_story_shiro_39(self):
        ret = self.Common_goto(2,0,1)#ポケセンターブルーへ移動
        if ret == "START":
            return "4_STORY_SHIRO_40"
        else:
            return "4_STORY_SHIRO_39"
    
    def _4_story_shiro_40(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,180), duration=3.2, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90), duration=8.0, wait=1.0)
            self.wait(0.5)
            return "4_STORY_SHIRO_41"
        return "4_STORY_SHIRO_40"
    
    def _4_story_shiro_41(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="3_SELECT",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.5):
                return "4_STORY_SHIRO_42"
        return "4_STORY_SHIRO_41"
    
    def _4_story_shiro_42(self):
        if self.image_check("3_SELECT"):
            for i in range(2):
                self.etc_sendCommand("Lbutton_down")
                self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=sleeptime):
                return "4_STORY_SHIRO_43"
        return "4_STORY_SHIRO_42"
    
    def _4_story_shiro_43(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            if self.image_check("FIELD1") or self.image_check("FIELD_BACK1"): 
                self.wait(0.5)
                self.etc_sendCommand("Lbutton_up")
                self.wait(4.0)
                #C+チェックをして、battle_Cp_loopでC+チェックを抜けるため
                self.ZL_ACTION("")
                self.battle_Cp_loop(Xaction=1,Aaction=0,Yaction=0,Baction=0)
                return "4_STORY_SHIRO_44"
            else:   
                self.etc_sendCommand("Lbutton_left")
                self.wait(0.5)
        return "4_STORY_SHIRO_43"
    
    def _4_story_shiro_44(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_45"
        return "4_STORY_SHIRO_44"
    
    def _4_story_shiro_45(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,70), duration=6.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,180), duration=0.5, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,270), duration=5.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,120), duration=4.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,340), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "4_STORY_SHIRO_46"
        return "4_STORY_SHIRO_45"
    
    def _4_story_shiro_46(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_47"
        return "4_STORY_SHIRO_46"
    
    def _4_story_shiro_47(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90-3), duration=13.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,0-3), duration=11.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90-3), duration=6.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,180-3), duration=5.5, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,90-3), duration=6.0, wait=1.0)
            self.wait(0.5)
            return "4_STORY_SHIRO_48"
        return "4_STORY_SHIRO_47"
    
    def _4_story_shiro_48(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_49"
        return "4_STORY_SHIRO_48"
    
    def _4_story_shiro_49(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "4_STORY_SHIRO_50"
        return "4_STORY_SHIRO_49"
    
    def _4_story_shiro_50(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="4_SELECT",sub5_button="A",sub5_picture="1_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_51"
        return "4_STORY_SHIRO_50"
    
    def _4_story_shiro_51(self):

        return "4_STORY_SHIRO_51"
    
    def _4_story_shiro_52(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.5, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,0), duration=8.0, wait=1.0)
            self.wait(0.5)
            return "4_STORY_SHIRO_53"
        return "4_STORY_SHIRO_52"
    
    def _4_story_shiro_53(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="4_SELECT",sub5_button="A",sub5_picture="1_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_54"
        return "4_STORY_SHIRO_53"
    
    def _4_story_shiro_54(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            if self.ball_change(2):#ハイパーボールチェック
                return "4_STORY_SHIRO_55"
        return "4_STORY_SHIRO_54"
    
    def _4_story_shiro_55(self):
        if self.battle_Cp_loop(Xaction=1,Aaction=1,Yaction=0,Baction=1,get_chanceicon4=1):
            return "4_STORY_SHIRO_55"
        return "4_STORY_SHIRO_55"
    #todo
    def _4_story_shiro_56(self):
        return "4_STORY_SHIRO_56"
    
    def _4_story_shiro_57(self):
        return "4_STORY_SHIRO_57"
    
    def _4_story_shiro_58(self):
        return "4_STORY_SHIRO_58"
    
    def _4_story_shiro_59(self):
        return "4_STORY_SHIRO_59"
    
    def _4_story_shiro_60(self):
        return "4_STORY_SHIRO_60"
    
    def _4_story_shiro_61(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=8.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,180), duration=8.0, wait=1.0)
            self.wait(0.5)
            return "4_STORY_SHIRO_62"
        return "4_STORY_SHIRO_61"
    
    def _4_story_shiro_62(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="4_SELECT",sub5_button="A",sub5_picture="1_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_63"
        return "4_STORY_SHIRO_62"
    
    def _4_story_shiro_63(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,30), duration=4.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "4_STORY_SHIRO_64"
        return "4_STORY_SHIRO_63"
    
    def _4_story_shiro_64(self):
        if self.image_check("TEXT_WHITE_COMMENT") or self.image_check("TEXT_BLACK_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="4_SELECT",sub5_button="A",sub5_picture="1_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_65"
        return "4_STORY_SHIRO_64"
    
    def _4_story_shiro_65(self):
        if self.markerdir("EVENT"):
            return "4_STORY_SHIRO_66"
        else:
            return "4_STORY_SHIRO_65"
    
    def _4_story_shiro_66(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,130), duration=3.5, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,220), duration=0.1, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "4_STORY_SHIRO_67"
        return "4_STORY_SHIRO_66"
    
    def _4_story_shiro_67(self):
        if self.image_check("TEXT_WHITE_COMMENT") or self.image_check("TEXT_BLACK_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="4_SELECT",sub5_button="A",sub5_picture="1_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_68"
        return "4_STORY_SHIRO_67"
    
    def _4_story_shiro_68(self):
        if self.markerdir("EVENT"):
            return "4_STORY_SHIRO_69"
        else:
            return "4_STORY_SHIRO_68"
    
    def _4_story_shiro_69(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,140), duration=3.5, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "4_STORY_SHIRO_70"
        return "4_STORY_SHIRO_69"
    
    def _4_story_shiro_70(self):
        if self.image_check("TEXT_WHITE_COMMENT") or self.image_check("TEXT_BLACK_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="4_SELECT",sub5_button="A",sub5_picture="1_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_71"
        return "4_STORY_SHIRO_70"
    
    def _4_story_shiro_71(self):
        if self.markerdir("EVENT"):
            return "4_STORY_SHIRO_72"
        else:
            return "4_STORY_SHIRO_71"
    
    def _4_story_shiro_72(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,130), duration=3.5, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "4_STORY_SHIRO_73"
        return "4_STORY_SHIRO_72"
    
    def _4_story_shiro_73(self):
        if self.image_check("TEXT_WHITE_COMMENT") or self.image_check("TEXT_BLACK_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="4_SELECT",sub5_button="A",sub5_picture="1_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_74"
        return "4_STORY_SHIRO_73"
    
    def _4_story_shiro_74(self):
        #AUTOSAVE
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,50), duration=6.0, wait=1.0)
            self.wait(0.5)
            return "4_STORY_SHIRO_75"
        return "4_STORY_SHIRO_74"
    
    def _4_story_shiro_75(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="4_SELECT",sub5_button="A",sub5_picture="1_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_76"
        return "4_STORY_SHIRO_75"
    
    def _4_story_shiro_76(self):
        #AUTOSAVE
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=6.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,180), duration=5.7, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,270), duration=6.0, wait=1.0)
            self.wait(0.5)
            return "4_STORY_SHIRO_77"
        return "4_STORY_SHIRO_76"
    
    def _4_story_shiro_77(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="4_SELECT",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="4_SELECT",sub5_button="A",sub5_picture="1_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_78"
        return "4_STORY_SHIRO_77"
    
    def _4_story_shiro_78(self):
        if self.image_check("4_SELECT"):
            self.wait(0.5)
            self.etc_sendCommand("Lbutton_down")
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)  
            return "4_STORY_SHIRO_79"
        return "4_STORY_SHIRO_78"
    
    def _4_story_shiro_79(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="4_SELECT",sub5_button="A",sub5_picture="1_SELECT",sleeptime=0.3):
                return "4_STORY_SHIRO_80"
        return "4_STORY_SHIRO_79"
    
    def _4_story_shiro_80(self):
        return self.story_Template_battle_before(noprg_ret="4_STORY_SHIRO_80",prg_ret="4_STORY_SHIRO_81",green_check=0)

    def _4_story_shiro_81(self):
        return self.story_Template_battle_function(bkprg_ret="4_STORY_SHIRO_80",prg_ret="4_STORY_SHIRO_82",noprg_ret="4_STORY_SHIRO_81",Xaction=1,Aaction=1,Yaction=0,Baction=1,lockon_endskip=0,get_chanceicon4=0,noCp=0)
    
    def _4_story_shiro_82(self):
        return self.story_Template_battle_after(bkprg_ret="4_STORY_SHIRO_81",prg_ret="4_STORY_SHIRO_83")
 
    def _4_story_shiro_83(self):
        ### AUTO_SAVE_POINT
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "4_STORY_SHIRO_84"
        else:
            return "4_STORY_SHIRO_83"
 
    def _4_story_shiro_84(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(1,0,-1)#ジャスティス会道場に移動で位置確定
        if ret == "START":
            return "4_STORY_SHIRO_85"
        else:
            return "4_STORY_SHIRO_84"
 
    def _4_story_shiro_85(self):
        #AUTOSAVE
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=6.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)  
            return "4_STORY_SHIRO_86"
        return "4_STORY_SHIRO_85"
 
    def _4_story_shiro_86(self):
        return self.story_Template_battle_before(noprg_ret="4_STORY_SHIRO_86",prg_ret="4_STORY_SHIRO_87",green_check=0)

    def _4_story_shiro_87(self):
        return self.story_Template_battle_function(bkprg_ret="4_STORY_SHIRO_86",prg_ret="4_STORY_SHIRO_88",noprg_ret="4_STORY_SHIRO_87",Xaction=1,Aaction=1,Yaction=0,Baction=1,lockon_endskip=0,get_chanceicon4=0,noCp=0)

    def _4_story_shiro_88(self):
        return self.story_Template_battle_after(bkprg_ret="4_STORY_SHIRO_87",prg_ret= "4_STORY_END")

    def _4_story_end(self):
        return "4_STORY_START_CHECK" 
    ######################################################
    # MAIN_5_D_LANK SUB FUNCTION
    ######################################################
    def _5_story_start_check(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            return "5_STORY_MAPPING_1"
        return "5_STORY_START_CHECK"

    def _5_story_mapping_1(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "5_STORY_MAPPING_2"
        else:
            return "5_STORY_MAPPING_1"
    
    def _5_story_mapping_2(self):
        ### AUTO_SAVE_POINT
        ret = self.Common_goto(2,0,3)#ポケセンターローズに移動で位置確定
        if ret == "START":
            return "5_STORY_MAPPING_3"
        else:
            return "5_STORY_MAPPING_2"

    def _5_story_mapping_3(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,0), duration=10.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,95), duration=7.5, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,0), duration=2.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "5_STORY_MAPPING_4"
        return "5_STORY_MAPPING_3"
        
    def _5_story_mapping_4(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_W_ZONE14"):
                print("MOVEPOINT_TARGET_W_ZONE14")
            if self.image_check("MOVEPOINT_PIC_W_ZONE14"):
                print("MOVEPOINT_PIC_W_ZONE14")
            
        else:
            ret = self.Common_goto(4,0,-1,movepoint_check=1)#Wゾーン14が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_W_ZONE14",pic2="MOVEPOINT_PIC_W_ZONE14") == True:
                    self.Common_goto_jump()
                    return "5_STORY_MAPPING_5"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "5_STORY_MAPPING_1"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "5_STORY_MAPPING_4"
            else:
                return "5_STORY_MAPPING_4"
        return "5_STORY_MAPPING_4"

    def _5_story_mapping_5(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(3,0,-4)#カフェアルティメットに移動で位置確定
        if ret == "START":
            return "5_STORY_MAPPING_6"
        else:
            return "5_STORY_MAPPING_5"
        
    #バトル対策が必要？
    def _5_story_mapping_6(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_W_ZONE15"):
                print("MOVEPOINT_TARGET_W_ZONE15")
            if self.image_check("MOVEPOINT_PIC_W_ZONE15"):
                print("MOVEPOINT_PIC_W_ZONE15")
            
        else:
            if self.image_check("EYE_CHECK_HIGH_POKE"):
                self.battle_Cp_loop(Xaction=0,Aaction=1,Yaction=0,Baction=1,mode=1)
                return "5_STORY_MAPPING_6"
            else:
                ret = self.Common_goto(4,0,-1,movepoint_check=1)#Wゾーン15が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_W_ZONE15",pic2="MOVEPOINT_PIC_W_ZONE15") == True:
                    #ゾーンから抜けたいのでずらす
                    self.etc_sendCommand("Lbutton_down")
                    self.wait(0.5)
                    self.Common_goto_jump()
                    return "5_STORY_D_LANK_BATTLE_ZONE"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "5_STORY_MAPPING_5"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "5_STORY_MAPPING_6"
            else:
                return "5_STORY_MAPPING_6"
        return "5_STORY_MAPPING_6"
    
    def _5_story_d_lank_battle_zone(self):
        self.battle_zone_loop_num = 1
        self.no_Cplus=0
        self.za_infi_main_current_state = self.STATE_ZA_INFI_MAIN_FUNCTION[self.za_infi_main_current_state]()
        self.wait(self.SLEEPLIST[9][2])
        if self.za_infi_main_current_state == "ZA_INFI_QUASAR_LOOP":
            self.za_infi_main_current_state = "ZA_INFI_MAIN_START"
            return "5_STORY_KARASUBA_1"
        else: 
            return "5_STORY_D_LANK_BATTLE_ZONE"
        
    def _5_story_karasuba_1(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "5_STORY_KARASUBA_2"
        else:
            return "5_STORY_KARASUBA_1"
    
    def _5_story_karasuba_2(self):
        ### AUTO_SAVE_POINT
        ret = self.Common_goto(4,0,4)#Wゾーン5に移動で位置確定
        if ret == "START":
            return "5_STORY_KARASUBA_3"
        else:
            return "5_STORY_KARASUBA_2"
    
    def _5_story_karasuba_3(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,200), duration=10.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,240), duration=2.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,160), duration=1.0, wait=0.5)
            self.wait(1.0)
            return "5_STORY_KARASUBA_4"
        return "5_STORY_KARASUBA_3"

    def _5_story_karasuba_4(self):
        return self.story_Template_battle_before(noprg_ret="5_STORY_KARASUBA_4",prg_ret="5_STORY_KARASUBA_5",green_check=0)
            
    def _5_story_karasuba_5(self):
        return self.story_Template_battle_function(bkprg_ret="5_STORY_KARASUBA_4",prg_ret="5_STORY_KARASUBA_6",noprg_ret="5_STORY_KARASUBA_5",Xaction=1,Aaction=1,Yaction=0,Baction=1,lockon_endskip=0,get_chanceicon4=0,noCp=0)

    def _5_story_karasuba_6(self):
        return self.story_Template_battle_after(bkprg_ret="5_STORY_KARASUBA_5",prg_ret= "5_STORY_KARASUBA_7")

    def _5_story_karasuba_7(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "5_STORY_KARASUBA_8"
        return "5_STORY_KARASUBA_7"
    
    def _5_story_karasuba_8(self):
        return self.story_Template_battle_before(noprg_ret="5_STORY_KARASUBA_8",prg_ret="5_STORY_KARASUBA_9",green_check=0)

    
    def _5_story_karasuba_9(self):
        return self.story_Template_battle_function(bkprg_ret="5_STORY_KARASUBA_8",prg_ret="5_STORY_KARASUBA_10",noprg_ret="5_STORY_KARASUBA_9",Xaction=1,Aaction=1,Yaction=0,Baction=1,lockon_endskip=0,get_chanceicon4=0,noCp=0)

    
    def _5_story_karasuba_10(self):
        return self.story_Template_battle_after(bkprg_ret="5_STORY_KARASUBA_9",prg_ret= "5_STORY_KARASUBA_11")

    
    def _5_story_karasuba_11(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=7.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "5_STORY_KARASUBA_12"
        return "5_STORY_KARASUBA_11"
    
    def _5_story_karasuba_12(self):
        if self.image_check("TEXT_BLACK_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="4_SELECT",sub5_button="A",sub5_picture="1_SELECT",sleeptime=0.3):
                return "5_STORY_KARASUBA_13"
        return "5_STORY_KARASUBA_12"
    
    def _5_story_karasuba_13(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=10.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "5_STORY_KARASUBA_14"
        return "5_STORY_KARASUBA_13"
    
    def _5_story_karasuba_14(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="4_SELECT",sub5_button="A",sub5_picture="1_SELECT",sleeptime=0.3):
                return "5_STORY_KARASUBA_15"
        return "5_STORY_KARASUBA_14"
    
    def _5_story_karasuba_15(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "5_STORY_KARASUBA_16"
        else:
            return "5_STORY_KARASUBA_15"
    
    def _5_story_karasuba_16(self):
        ret = self.Common_goto(1,0,3)#ホテルZへ移動
        if ret == "START":
            return "5_STORY_KARASUBA_17"
        else:
            return "5_STORY_KARASUBA_16"
    
    def _5_story_karasuba_17(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "5_STORY_KARASUBA_18"
        return "5_STORY_KARASUBA_17"
    
    def _5_story_karasuba_18(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                self.wait(1.0)
                return "5_STORY_KARASUBA_19"
        return "5_STORY_KARASUBA_18"
    
    def _5_story_karasuba_19(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,35), duration=3.0, wait=1.0)
            self.wait(0.5)
            self.press(Direction(Stick.LEFT,270), duration=0.7, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "5_STORY_KARASUBA_20"
        return "5_STORY_KARASUBA_19"
    
    def _5_story_karasuba_20(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="3_SELECT",sub3_button="A",sub3_picture="2_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                self.wait(1.0)
                return "5_STORY_KARASUBA_21"
        return "5_STORY_KARASUBA_20"
    
    def _5_story_karasuba_21(self):
        #クチート
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "5_STORY_KARASUBA_22"
        else:
            return "5_STORY_KARASUBA_21"
            
    def _5_story_karasuba_22(self):
        ret = self.Common_goto(4,0,-2)#Wゾーン14へ移動
        if ret == "START":
            return "5_STORY_KARASUBA_23"
        else:
            return "5_STORY_KARASUBA_22"
    
    def _5_story_karasuba_23(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,180), duration=9.0, wait=1.0)
            self.press(Direction(Stick.LEFT,70), duration=19.0, wait=1.0)
            self.press(Direction(Stick.LEFT,90), duration=1.5, wait=1.0)
            self.press(Direction(Stick.LEFT,70), duration=5.5, wait=1.0)
            self.press(Direction(Stick.LEFT,330), duration=5.0, wait=1.0)
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=1.0)
            self.press(Direction(Stick.LEFT,230), duration=0.3, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=1.0, interval=0.1)
            self.press(Direction(Stick.LEFT,90), duration=4.0, wait=1.0)
            self.ROTOM_GLIDE(dir=90,a_count=20,a_wait=2.0)
            self.press(Direction(Stick.LEFT,180), duration=0.4, wait=1.0)
            self.press(Direction(Stick.LEFT,90), duration=1.0, wait=1.0)
            self.press(Direction(Stick.LEFT,350), duration=0.4, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=1.0, interval=0.1)
            self.press(Direction(Stick.LEFT,90), duration=3.0, wait=1.0)
            self.press(Direction(Stick.LEFT,180), duration=0.6, wait=1.0)
            self.press(Direction(Stick.LEFT,80), duration=4.0, wait=1.0)
            self.press(Direction(Stick.LEFT,0), duration=4.0, wait=1.0)
            self.press(Direction(Stick.LEFT,270), duration=2.5, wait=1.0)
            self.press(Direction(Stick.LEFT,0), duration=2.0, wait=1.0)
            return "5_STORY_KARASUBA_24"
        return "5_STORY_KARASUBA_23"
    
    def _5_story_karasuba_24(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_25"
        return "5_STORY_KARASUBA_24"
    
    def _5_story_karasuba_25(self):
        if self.mega_evolution_battle_mode_select(mode=0):
            return "5_STORY_KARASUBA_26"
        return "5_STORY_KARASUBA_25"
    
    def _5_story_karasuba_26(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_27"
        return "5_STORY_KARASUBA_26"
    
    def _5_story_karasuba_27(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "5_STORY_KARASUBA_28"
        else:
            return "5_STORY_KARASUBA_27"
    
    def _5_story_karasuba_28(self):
        ret = self.Common_goto(3,1,0)#ヌーヴォカフェ2号へ移動
        if ret == "START":
            return "5_STORY_KARASUBA_29"
        else:
            return "5_STORY_KARASUBA_28"
    
    def _5_story_karasuba_29(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,10), duration=4.3, wait=1.0)
            self.press(Direction(Stick.LEFT,270), duration=10.0, wait=1.0)
            self.press(Direction(Stick.LEFT,180), duration=1.8, wait=1.0)
            self.press(Direction(Stick.LEFT,90), duration=5.5, wait=1.0)
            self.press(Direction(Stick.LEFT,0), duration=4.0, wait=1.0)
            self.press(Direction(Stick.LEFT,270), duration=3.2, wait=1.0)
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=1.0, interval=0.1)
            self.wait(1.0)
            self.etc_sendCommand("Lbutton_up")
            self.wait(1.0)
            for i in range(3):
                self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=10.0, wait=1.0)
            return "5_STORY_KARASUBA_30"
        return "5_STORY_KARASUBA_29"
    
    def _5_story_karasuba_30(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_31"
        elif self.markerdir("EVENT"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            return "5_STORY_KARASUBA_30"
        return "5_STORY_KARASUBA_30"
    
    def _5_story_karasuba_31(self):
        if self.mega_evolution_battle_mode_select(mode=0):
            return "5_STORY_KARASUBA_32"
        return "5_STORY_KARASUBA_31"
    
    def _5_story_karasuba_32(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_33"
        return "5_STORY_KARASUBA_32"
    
    def _5_story_karasuba_33(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_34"
        return "5_STORY_KARASUBA_33"

    def _5_story_karasuba_34(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "5_STORY_KARASUBA_35"
        else:
            return "5_STORY_KARASUBA_34"
    
    def _5_story_karasuba_35(self):
        ret = self.Common_goto(3,0,-2)#カフェパルトネールへ移動
        if ret == "START":
            return "5_STORY_KARASUBA_36"
        else:
            return "5_STORY_KARASUBA_35"
        
    def _5_story_karasuba_36(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,240), duration=8.0, wait=1.0)
            self.press(Direction(Stick.LEFT,310), duration=9.0, wait=1.0)
            self.press(Direction(Stick.LEFT,220), duration=4.0, wait=1.0)
            return "5_STORY_KARASUBA_37"
        return "5_STORY_KARASUBA_36"
    
    def _5_story_karasuba_37(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_38"
        return "5_STORY_KARASUBA_37"

    def _5_story_karasuba_38(self):
        #ムクに話しかける
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,88), duration=0.8, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=1.0, interval=0.1)
            return "5_STORY_KARASUBA_39"
        return "5_STORY_KARASUBA_38"
    
    def _5_story_karasuba_39(self):
        return self.story_Template_battle_before(noprg_ret="5_STORY_KARASUBA_39",prg_ret="5_STORY_KARASUBA_40",green_check=0)
    
    def _5_story_karasuba_40(self):
        return self.story_Template_battle_function(bkprg_ret="5_STORY_KARASUBA_39",prg_ret="5_STORY_KARASUBA_41",noprg_ret="5_STORY_KARASUBA_40",Xaction=1,Aaction=1,Yaction=0,Baction=1,lockon_endskip=0,get_chanceicon4=0,noCp=0)
    
    def _5_story_karasuba_41(self):
        return self.story_Template_battle_after(bkprg_ret="5_STORY_KARASUBA_40",prg_ret= "5_STORY_KARASUBA_42")
    
    def _5_story_karasuba_42(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=0.7, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=1.0, interval=0.1)
            return "5_STORY_KARASUBA_43"
        return "5_STORY_KARASUBA_42"
    
    def _5_story_karasuba_43(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.press(Direction(Stick.LEFT,180), duration=8.0, wait=1.0)
            self.press(Direction(Stick.LEFT,270), duration=4.0, wait=1.0)
            self.press(Direction(Stick.LEFT,235), duration=10.0, wait=1.0)
            self.press(Direction(Stick.LEFT,145), duration=0.5, wait=1.0)
            self.press(Direction(Stick.LEFT,260), duration=1.5, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=1.0, interval=0.1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=3.0, wait=2.0)
            self.press(Direction(Stick.LEFT,90), duration=2.2, wait=1.0)
            self.press(Direction(Stick.LEFT,348), duration=7.0, wait=1.0) 
            self.press(Direction(Stick.LEFT,320), duration=0.3, wait=1.0) 
            
            self.pressRep(Button.L, repeat=1, duration=0.15, wait=1.0, interval=0.1)
            self.wait(1.0)
            self.etc_sendCommand("Lbutton_up")
            self.wait(1.0)
            for i in range(3):
                self.battle_coCp_noloop(Xaction=0,Aaction=1,Yaction=0,Baction=1)
            self.wait(2.0)
            
            return "5_STORY_KARASUBA_44"
        return "5_STORY_KARASUBA_43"
    
    def _5_story_karasuba_44(self):
        if self.markerdir("EVENT"):
            self.press(Direction(Stick.LEFT,100), duration=0.4, wait=2.0)    
            self.press(Direction(Stick.LEFT,220), duration=0.8, wait=1.0)
            self.press(Direction(Stick.LEFT,130), duration=0.1, wait=2.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=1.0, interval=0.1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=2.5, wait=2.0)
            
            self.press(Direction(Stick.LEFT,130), duration=3.0, wait=2.0)
            self.press(Direction(Stick.LEFT,110), duration=2.0, wait=2.0)
            self.press(Direction(Stick.LEFT,115), duration=2.0, wait=2.0)
            
            self.press(Direction(Stick.LEFT,53), duration=2.5, wait=2.0)
            self.press(Direction(Stick.LEFT,320), duration=4.0, wait=2.0)
            self.press(Direction(Stick.LEFT,340), duration=10.0, wait=2.0)
            
            self.press(Direction(Stick.LEFT,270), duration=4.0, wait=2.0)
            self.press(Direction(Stick.LEFT,340), duration=5.0, wait=2.0)
            
            self.press(Direction(Stick.LEFT,270), duration=4.0, wait=2.0)
            self.press(Direction(Stick.LEFT,340), duration=5.0, wait=2.0)

            return "5_STORY_KARASUBA_45"
        return "5_STORY_KARASUBA_44"
    
    def _5_story_karasuba_45(self):
        if self.markerdir("EVENT"):
            self.press(Direction(Stick.LEFT,50), duration=4.0, wait=2.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=1.0, interval=0.1)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=4.0, wait=2.0)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=6.0, wait=2.0)
            return "5_STORY_KARASUBA_46"
        return "5_STORY_KARASUBA_45"
    
    def _5_story_karasuba_46(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_47"
        return "5_STORY_KARASUBA_46"

    def _5_story_karasuba_47(self):
        if self.mega_evolution_battle_mode_select(mode=0):
            return "5_STORY_KARASUBA_48"
        return "5_STORY_KARASUBA_47"
    
    def _5_story_karasuba_48(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_49"
        return "5_STORY_KARASUBA_48"
    
    def _5_story_karasuba_49(self):
        self.common_item_give_current_state = self.common_item_give_function(selectnum=4,target1=4,target2=2)
        if self.common_item_give_current_state == "COMMON_ITEM_GIVE_START":
            return "5_STORY_KARASUBA_50"
        else:
            return "5_STORY_KARASUBA_49"
    
    def _5_story_karasuba_50(self):
        ret = self.Common_goto(1,0,3)#ホテルZへ移動
        if ret == "START":
            return "5_STORY_KARASUBA_51"
        else:
            return "5_STORY_KARASUBA_50"
    
    def _5_story_karasuba_51(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "5_STORY_KARASUBA_52"
        return "5_STORY_KARASUBA_51"
    
    def _5_story_karasuba_52(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="ODAIRU_ICON",endpicture2="ABSOL_ICON",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_53"

        return "5_STORY_KARASUBA_52"
    
    def _5_story_karasuba_53(self):
        ret = self.Common_goto(3,0,5)#カフェソレイユへ移動
        if ret == "START":
            return "5_STORY_KARASUBA_54"
        else:
            return "5_STORY_KARASUBA_53"
    
    def _5_story_karasuba_54(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,0), duration=3.0, wait=1.0)
            self.press(Direction(Stick.LEFT,90), duration=8.0, wait=1.0)
            self.press(Direction(Stick.LEFT,0), duration=2.0, wait=1.0)
            return "5_STORY_KARASUBA_55"
        return "5_STORY_KARASUBA_54"
    
    def _5_story_karasuba_55(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_56"
        return "5_STORY_KARASUBA_55"
    
    def _5_story_karasuba_56(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=0.5, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "5_STORY_KARASUBA_57"
        return "5_STORY_KARASUBA_56"

    def _5_story_karasuba_57(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_58"
        return "5_STORY_KARASUBA_57"
    
    def _5_story_karasuba_58(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,110), duration=3.0, wait=1.0)
            return "5_STORY_KARASUBA_59"
        return "5_STORY_KARASUBA_58"
    
    def _5_story_karasuba_59(self):
        self.no_Cplus=0
        if self.battle_Cp_loop(Xaction=1,Aaction=1,Yaction=0,Baction=1,mode=1,battle_mode=1):
            if not self.image_check("EYE_CHECK_HIGH_POKE"):
                return "5_STORY_KARASUBA_60"
        return "5_STORY_KARASUBA_59"
    
    def _5_story_karasuba_60(self):
        if self.image_check("EYE_CHECK_HIGH_POKE"):
            return "5_STORY_KARASUBA_59"
        elif self.markerdir("EVENT"):
            return "5_STORY_KARASUBA_61"
        return "5_STORY_KARASUBA_60"
    
    def _5_story_karasuba_61(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,80), duration=2.0, wait=1.0)
            self.press(Direction(Stick.LEFT,100), duration=2.0, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "5_STORY_KARASUBA_62"
        return "5_STORY_KARASUBA_61"
    
    def _5_story_karasuba_62(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_63"
        return "5_STORY_KARASUBA_62"
    
    def _5_story_karasuba_63(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "5_STORY_KARASUBA_64"
        else:
            return "5_STORY_KARASUBA_63"
    
    def _5_story_karasuba_64(self):
        ret = self.Common_goto(2,0,3)#ポケセンターローズへ移動
        if ret == "START":
            return "5_STORY_KARASUBA_65"
        else:
            return "5_STORY_KARASUBA_64"
    
    def _5_story_karasuba_65(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,0), duration=3.5, wait=1.0)
            self.press(Direction(Stick.LEFT,90), duration=14.5, wait=1.0)
            self.press(Direction(Stick.LEFT,180), duration=0.7, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "5_STORY_KARASUBA_66"
        return "5_STORY_KARASUBA_65"
    
    def _5_story_karasuba_66(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_67"
        return "5_STORY_KARASUBA_66"
    
    def _5_story_karasuba_67(self):
        if self.image_check("IN_ICON"):
            self.press(Direction(Stick.LEFT,90), duration=0.5, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "5_STORY_KARASUBA_68"
        return "5_STORY_KARASUBA_67"
    
    def _5_story_karasuba_68(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_69"
        return "5_STORY_KARASUBA_68"
    
    def _5_story_karasuba_69(self):
        #失敗時に戻れるように
        ret = self.Common_goto(0,0,0,othermap="UG_SEWER_MAP")#地下水道入口へ移動
        if ret == "START":
            return "5_STORY_KARASUBA_70"
        else:
            return "5_STORY_KARASUBA_69"
    
    def _5_story_karasuba_70(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            if self.image_check("FIELD2") or self.image_check("FIELD_BACK2"):
                self.etc_sendCommand("Lbutton_up")
                self.wait(1.0)
                if self.image_check("FIELD_BACK_W"):
                    return "5_STORY_KARASUBA_71"                
            else:
                self.etc_sendCommand("Lbutton_left")
                self.wait(1.0)
        return "5_STORY_KARASUBA_70"
    
    def _5_story_karasuba_71(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=3.0, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "5_STORY_KARASUBA_72"
        return "5_STORY_KARASUBA_71"
    
    def _5_story_karasuba_72(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            self.wait(1.0)
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)

            if not self.image_check("EYE_CHECK_HIGH_POKE"):
                self.wait(2.0)
                return "5_STORY_KARASUBA_73"
        return "5_STORY_KARASUBA_72"
    
    def _5_story_karasuba_73(self):
        if self.markerdir("EVENT"):
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                self.press(Direction(Stick.LEFT,250), duration=2.0, wait=1.0)
                self.pressRep(Button.L, repeat=1, duration=0.15, wait=1.0, interval=0.1)
                return "5_STORY_KARASUBA_74" 
        return "5_STORY_KARASUBA_73"
    
    def _5_story_karasuba_74(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            self.wait(1.0)
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            if not self.image_check("EYE_CHECK_HIGH_POKE"):
                self.wait(2.0)
                return "5_STORY_KARASUBA_75"
        return "5_STORY_KARASUBA_74"
    
    def _5_story_karasuba_75(self):
        if self.markerdir("EVENT"):
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                self.press(Direction(Stick.LEFT,290), duration=3.0, wait=1.0)
                self.press(Direction(Stick.LEFT,330), duration=1.0, wait=1.0)#?
                self.pressRep(Button.L, repeat=1, duration=0.15, wait=1.0, interval=0.1)
                return "5_STORY_KARASUBA_76" 
        return "5_STORY_KARASUBA_75"
    
    def _5_story_karasuba_76(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            self.wait(1.0)
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            if not self.image_check("EYE_CHECK_HIGH_POKE"):
                self.wait(2.0)
                return "5_STORY_KARASUBA_77"
        return "5_STORY_KARASUBA_76"
    
    def _5_story_karasuba_77(self):
        if self.markerdir("EVENT"):
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                self.press(Direction(Stick.LEFT,20), duration=1.0, wait=1.0)
                self.pressRep(Button.L, repeat=1, duration=0.15, wait=1.0, interval=0.1)
                return "5_STORY_KARASUBA_78" 
        return "5_STORY_KARASUBA_77"
    
    def _5_story_karasuba_78(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            self.wait(1.0)
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            if not self.image_check("EYE_CHECK_HIGH_POKE"):
                self.wait(2.0)
                return "5_STORY_KARASUBA_79"
        return "5_STORY_KARASUBA_78"
    
    def _5_story_karasuba_79(self):
        if self.markerdir("EVENT"):
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                self.press(Direction(Stick.LEFT,290), duration=2.5, wait=1.0)
                self.press(Direction(Stick.LEFT,330), duration=0.1, wait=1.0)
                self.pressRep(Button.L, repeat=1, duration=0.15, wait=1.0, interval=0.1)
                return "5_STORY_KARASUBA_80" 
        return "5_STORY_KARASUBA_79"
    
    def _5_story_karasuba_80(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            self.wait(1.0)
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            if not self.image_check("EYE_CHECK_HIGH_POKE"):
                self.wait(2.0)
                return "5_STORY_KARASUBA_81"
        return "5_STORY_KARASUBA_80"
    
    def _5_story_karasuba_81(self):
        if self.markerdir("EVENT"):
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                self.press(Direction(Stick.LEFT,130), duration=4.0, wait=1.0)
                self.press(Direction(Stick.LEFT,230), duration=4.0, wait=1.0)
                self.pressRep(Button.L, repeat=1, duration=0.15, wait=1.0, interval=0.1)
                return "5_STORY_KARASUBA_82" 
        return "5_STORY_KARASUBA_81"
    
    def _5_story_karasuba_82(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            self.wait(1.0)
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            if not self.image_check("EYE_CHECK_HIGH_POKE"):
                self.wait(2.0)
                return "5_STORY_KARASUBA_83"
        return "5_STORY_KARASUBA_82"
    
    def _5_story_karasuba_83(self):
        if self.markerdir("EVENT"):
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                self.press(Direction(Stick.LEFT,330), duration=0.1, wait=1.0)
                self.pressRep(Button.L, repeat=1, duration=0.15, wait=1.0, interval=0.1)
                return "5_STORY_KARASUBA_84" 
        return "5_STORY_KARASUBA_83"
    
    def _5_story_karasuba_84(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            self.wait(1.0)
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            if not self.image_check("EYE_CHECK_HIGH_POKE"):
                self.wait(2.0)
                return "5_STORY_KARASUBA_85"
        return "5_STORY_KARASUBA_84"
    
    def _5_story_karasuba_85(self):
        if self.markerdir("EVENT"):
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                self.press(Direction(Stick.LEFT,270), duration=1.5, wait=1.0)
                self.pressRep(Button.L, repeat=1, duration=0.15, wait=1.0, interval=0.1)
                return "5_STORY_KARASUBA_86" 
        return "5_STORY_KARASUBA_85"
    
    def _5_story_karasuba_86(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            self.wait(1.0)
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            if not self.image_check("EYE_CHECK_HIGH_POKE"):
                self.wait(2.0)
                return "5_STORY_KARASUBA_87"
        return "5_STORY_KARASUBA_86"
    
    def _5_story_karasuba_87(self):
        if self.markerdir("EVENT"):
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                self.press(Direction(Stick.LEFT,270), duration=1.0, wait=1.0)
                self.press(Direction(Stick.LEFT,0), duration=4.5, wait=1.0)
                self.pressRep(Button.L, repeat=1, duration=0.15, wait=1.0, interval=0.1)
                return "5_STORY_KARASUBA_88" 
        return "5_STORY_KARASUBA_87"
    
    def _5_story_karasuba_88(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            self.wait(1.0)
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            if not self.image_check("EYE_CHECK_HIGH_POKE"):
                self.wait(2.0)
                return "5_STORY_KARASUBA_89"
        return "5_STORY_KARASUBA_88"
    
    def _5_story_karasuba_89(self):
        if self.markerdir("EVENT"):
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                self.press(Direction(Stick.LEFT,70), duration=0.1, wait=1.0)
                self.pressRep(Button.L, repeat=1, duration=0.15, wait=1.0, interval=0.1)
                return "5_STORY_KARASUBA_90" 
        return "5_STORY_KARASUBA_89"
    
    def _5_story_karasuba_90(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            self.wait(1.0)
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            if not self.image_check("EYE_CHECK_HIGH_POKE"):
                self.wait(2.0)
                return "5_STORY_KARASUBA_91"
        return "5_STORY_KARASUBA_90"
    
    def _5_story_karasuba_91(self):
        if self.markerdir("EVENT"):
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                self.press(Direction(Stick.LEFT,0), duration=0.5, wait=1.0)
                self.press(Direction(Stick.LEFT,260), duration=4.0, wait=1.0)
                self.press(Direction(Stick.LEFT,30), duration=0.1, wait=1.0)
                self.pressRep(Button.L, repeat=1, duration=0.15, wait=1.0, interval=0.1)
                return "5_STORY_KARASUBA_92" 
        return "5_STORY_KARASUBA_91"
    
    def _5_story_karasuba_92(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            self.wait(1.0)
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            if not self.image_check("EYE_CHECK_HIGH_POKE"):
                self.wait(2.0)
                return "5_STORY_KARASUBA_93"
        return "5_STORY_KARASUBA_92"
    
    def _5_story_karasuba_93(self):
        if self.markerdir("EVENT"):
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                self.press(Direction(Stick.LEFT,235), duration=1.8, wait=1.0)
                self.pressRep(Button.L, repeat=1, duration=0.15, wait=1.0, interval=0.1)
                self.wait(2.0)
                self.press(Direction(Stick.RIGHT,90), duration=0.3, wait=1.0)
                return "5_STORY_KARASUBA_94" 
        return "5_STORY_KARASUBA_93"
    
    def _5_story_karasuba_94(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            self.wait(1.0)
            self.battle_coCp_noloop(Xaction=0,Aaction=0,Yaction=0,Baction=1,battle_mode=1)
            if not self.image_check("EYE_CHECK_HIGH_POKE"):
                self.wait(2.0)
                return "5_STORY_KARASUBA_95"
        return "5_STORY_KARASUBA_94"
    
    def _5_story_karasuba_95(self):
        if self.image_check("TEXT_BLACK_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_96"
        return "5_STORY_KARASUBA_95"
    
    def _5_story_karasuba_96(self):
        ret = self.Common_goto(0,0,0,othermap="UG_SEWER_MAP")#地下水道入口へ移動
        if ret == "START":
            return "5_STORY_KARASUBA_97"
        else:
            return "5_STORY_KARASUBA_96"
    
    def _5_story_karasuba_97(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,70), duration=0.8, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=1.0, interval=0.1)
            return "5_STORY_KARASUBA_98" 
        return "5_STORY_KARASUBA_97"
    
    def _5_story_karasuba_98(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_99"
        return "5_STORY_KARASUBA_98"
    
    def _5_story_karasuba_99(self):
        ret = self.Common_change_time_set(check_timing="NIGHT")#時間変更前のためとりあえず時間変更とする
        if ret == "START":
            return "5_STORY_KARASUBA_100"
        else:
            return "5_STORY_KARASUBA_99"
    
    def _5_story_karasuba_100(self):
        ret = self.Common_goto(2,0,-3)#ポケセンメディオに移動で位置確定
        if ret == "START":
            return "5_STORY_KARASUBA_101"
        else:
            return "5_STORY_KARASUBA_100"
    
    def _5_story_karasuba_101(self):
        ### AUTO_SAVE_POINT
        if self.Common_pokemon_recovery():
            return "5_STORY_KARASUBA_102"
        else:
            return "5_STORY_KARASUBA_101"
    
    def _5_story_karasuba_102(self):
        ret = self.Common_goto(2,0,-3)#ポケセンメディオに移動で位置確定
        if ret == "START":
            return "5_STORY_KARASUBA_103"
        else:
            return "5_STORY_KARASUBA_102"
    
    def _5_story_karasuba_103(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,260), duration=9.0, wait=1.0)
            return "5_STORY_KARASUBA_104"
        return "5_STORY_KARASUBA_103"
    
    def _5_story_karasuba_104(self):
        return self.story_Template_battle_before(noprg_ret="5_STORY_KARASUBA_104",prg_ret="5_STORY_KARASUBA_105",green_check=0)
    
    def _5_story_karasuba_105(self):
        # 連戦をどちらもこちらで対応(106に行った後、105に戻るため)
        return self.story_Template_battle_function(bkprg_ret="5_STORY_KARASUBA_104",prg_ret="5_STORY_KARASUBA_106",noprg_ret="5_STORY_KARASUBA_105",Xaction=1,Aaction=1,Yaction=0,Baction=1,lockon_endskip=0,get_chanceicon4=0,noCp=0)
    
    def _5_story_karasuba_106(self):
        return self.story_Template_battle_after(bkprg_ret="5_STORY_KARASUBA_105",prg_ret= "5_STORY_KARASUBA_107")
    
    def _5_story_karasuba_107(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            #バックアップから戻る場合に角度が変わるため
            if self.markerdir("EVENT"):
                self.press(Direction(Stick.LEFT,135), duration=5.0, wait=1.0)
                self.press(Direction(Stick.LEFT,60), duration=8.0, wait=1.0)
                return "5_STORY_KARASUBA_108"
        return "5_STORY_KARASUBA_107"
    
    def _5_story_karasuba_108(self):
        return self.story_Template_battle_before(noprg_ret="5_STORY_KARASUBA_108",prg_ret="5_STORY_KARASUBA_109",green_check=0)

    
    def _5_story_karasuba_109(self):
        return self.story_Template_battle_function(bkprg_ret="5_STORY_KARASUBA_108",prg_ret="5_STORY_KARASUBA_110",noprg_ret="5_STORY_KARASUBA_109",Xaction=1,Aaction=1,Yaction=0,Baction=1,lockon_endskip=0,get_chanceicon4=0,noCp=0)

    
    def _5_story_karasuba_110(self):
        return self.story_Template_battle_after(bkprg_ret="5_STORY_KARASUBA_109",prg_ret= "5_STORY_KARASUBA_111")

    def _5_story_karasuba_111(self):
        ret = self.Common_change_time_set(check_timing="NIGHT")#時間変更前のためとりあえず時間変更とする
        if ret == "START":
            return "5_STORY_KARASUBA_112"
        else:
            return "5_STORY_KARASUBA_111"

    def _5_story_karasuba_112(self):
        ret = self.Common_goto(2,0,-3)#ポケセンメディオに移動で位置確定
        if ret == "START":
            return "5_STORY_KARASUBA_113"
        else:
            return "5_STORY_KARASUBA_112"

    def _5_story_karasuba_113(self):
        ### AUTO_SAVE_POINT
        if self.Common_pokemon_recovery():
            return "5_STORY_KARASUBA_114"
        else:
            return "5_STORY_KARASUBA_113"

    def _5_story_karasuba_114(self):
        ret = self.Common_goto(1,0,3)#ホテルZへ移動
        if ret == "START":
            return "5_STORY_KARASUBA_115"
        else:
            return "5_STORY_KARASUBA_114"

    def _5_story_karasuba_115(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.wait(0.5)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "5_STORY_KARASUBA_116"
        return "5_STORY_KARASUBA_115"

    def _5_story_karasuba_116(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_117"
        return "5_STORY_KARASUBA_116"

    def _5_story_karasuba_117(self):
        ret = self.Common_goto(1,1,0)#サビ組事務所へ移動
        if ret == "START":
            return "5_STORY_KARASUBA_118"
        else:
            return "5_STORY_KARASUBA_117"

    def _5_story_karasuba_118(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=7.0, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "5_STORY_KARASUBA_119"
        return "5_STORY_KARASUBA_118"

    def _5_story_karasuba_119(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=10.0, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "5_STORY_KARASUBA_120"
        return "5_STORY_KARASUBA_119"

    def _5_story_karasuba_120(self):
        if self.image_check("TEXT_WHITE_COMMENT"):
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="2_SELECT",sub3_button="A",sub3_picture="3_SELECT",sub4_button="A",sub4_picture="HELP_MARKER",sleeptime=0.5):
                return "5_STORY_KARASUBA_121"
        return "5_STORY_KARASUBA_120"

    def _5_story_karasuba_121(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT,90), duration=2.0, wait=1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "5_STORY_KARASUBA_122"
        return "5_STORY_KARASUBA_121"

    def _5_story_karasuba_122(self):
        return self.story_Template_battle_before(noprg_ret="5_STORY_KARASUBA_122",prg_ret="5_STORY_KARASUBA_123",green_check=0)

    def _5_story_karasuba_123(self):
        return self.story_Template_battle_function(bkprg_ret="5_STORY_KARASUBA_122",prg_ret="5_STORY_KARASUBA_124",noprg_ret="5_STORY_KARASUBA_123",Xaction=1,Aaction=1,Yaction=0,Baction=1,lockon_endskip=0,get_chanceicon4=0,noCp=0)

    def _5_story_karasuba_124(self):
        ret = self.story_Template_battle_after(bkprg_ret="5_STORY_KARASUBA_123",prg_ret= "5_STORY_END")
        if ret == "5_STORY_END":
            #誤判定用のガード
            if self.image_check("ODAIRU_ICON") or self.image_check("ABSOL_ICON"):
                return "5_STORY_END"
        elif ret == "5_STORY_KARASUBA_123":
            return "5_STORY_KARASUBA_123"    
        return "5_STORY_KARASUBA_124"
    
    def _5_story_end(self):
        return "5_STORY_START_CHECK"
    
    ######################################################
    # MAIN_6_C_LANK SUB FUNCTION
    ######################################################
    def _6_story_start_check(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            return "6_STORY_MAPPING_1"
        return "6_STORY_START_CHECK"
    
    def _6_story_mapping_1(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_change_time_set(check_timing="MORNING")
        if ret == "START":
            return "6_STORY_MAPPING_2"
        else:
            return "6_STORY_MAPPING_1"
    
    def _6_story_mapping_2(self):
        ### AUTO_SAVE_POINT
        #失敗時に再実施できるようにマップ移動から開始する。
        ret = self.Common_goto(2,0,0)#ポケセンターベールに移動で位置確定
        if ret == "START":
            return "6_STORY_MAPPING_3"
        else:
            return "6_STORY_MAPPING_2"
    
    def _6_story_mapping_3(self):
        ### AUTO_SAVE_POINT
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,0), duration=4.0, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,90), duration=7.5, wait=0.5)
            self.wait(1.0)
            self.press(Direction(Stick.LEFT,0), duration=2.0, wait=0.5)
            self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            return "6_STORY_MAPPING_4"
        return "6_STORY_MAPPING_3"
    
    def _6_story_mapping_4(self):
        if self.check_picture==1:
            if self.image_check("MOVEPOINT_TARGET_W_ZONE17"):
                print("MOVEPOINT_TARGET_W_ZONE17")
            if self.image_check("MOVEPOINT_PIC_W_ZONE17"):
                print("MOVEPOINT_PIC_W_ZONE17")
            
        else:
            ret = self.Common_goto(4,0,-1,movepoint_check=1)#Wゾーン14が登録されたか確認
            
            if ret == "MOVEPOINT_PIC":
                self.wait(1.0)
                if self.Common_mappic_check(pic1="MOVEPOINT_TARGET_W_ZONE17",pic2="MOVEPOINT_PIC_W_ZONE17") == True:
                    self.Common_goto_jump()
                    return "6_STORY_C_LANK_BATTLE_ZONE"
                else:
                    #登録できていない場合、移動元からやり直し
                    self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                    return "6_STORY_MAPPING_1"
            elif ret == "START":
                #想定外にこちらに来た場合は開きなおし
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.5, interval=0.1)
                return "6_STORY_MAPPING_4"
            else:
                return "6_STORY_MAPPING_4"
        return "6_STORY_MAPPING_4"
    
    def _6_story_c_lank_battle_zone(self):
        self.battle_zone_loop_num = 1
        self.no_Cplus=0
        self.za_infi_main_current_state = self.STATE_ZA_INFI_MAIN_FUNCTION[self.za_infi_main_current_state]()
        self.wait(self.SLEEPLIST[9][2])
        if self.za_infi_main_current_state == "ZA_INFI_QUASAR_LOOP":
            self.za_infi_main_current_state = "ZA_INFI_MAIN_START"
            return "6_STORY_YUKARI_1"
        else: 
            return "6_STORY_C_LANK_BATTLE_ZONE"
       
    
    def _6_story_end(self):
        return "6_STORY_START_CHECK"
    
    # #TODO
    ######################################################
    # MAIN_7_B_LANK SUB FUNCTION
    ######################################################
    def _7_story_start_check(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            return "5_STORY_MAPPING_1"
        return "7_STORY_START_CHECK"
    
    def _7_story_end(self):
        return "7_STORY_START_CHECK"

    ######################################################
    # MAIN_8_STORY_LAST SUB FUNCTION
    ######################################################
    def _8_story_start_check(self):
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            return "5_STORY_MAPPING_1"
        return "8_STORY_START_CHECK"
    
    def _8_story_end(self):
        return "8_STORY_START_CHECK"

    ######################################################
    # Commonfunction
    ######################################################
    ######################################################
    # Commonskill
    ######################################################
    def common_skill_change_function(self,selectpokemonnum,target1,target2,machine=0):
        if self.common_skill_change_current_state == "COMMON_SKILL_CHANGE_POKEMON_SELECT":
            self.common_skill_change_current_state = self.common_skill_change_pokemon_select(selectnum=selectpokemonnum)
        elif self.common_skill_change_current_state == "COMMON_SKILL_CHANGE_SKILL_WINDOW_CHTARGET1":
            self.common_skill_change_current_state = self.common_skill_change_skill_window_chtarget1(target1=target1,machine=machine)
        elif self.common_skill_change_current_state == "COMMON_SKILL_CHANGE_SKILL_WINDOW_CHTARGET2":
            self.common_skill_change_current_state = self.common_skill_change_skill_window_chtarget2(target2=target2)
        else:
            self.common_skill_change_current_state = self.STATE_COMMON_SKILL_CHANGE_FUNCTION[self.common_skill_change_current_state]()

        return self.common_skill_change_current_state

    def common_skill_change_start(self):
        return "COMMON_SKILL_CHANGE_START_CHECK"
            
    def common_skill_change_start_check(self):
        if self.check_picture==1:
            if self.image_check("X_MENU_OPEN"):
                print("X_MENU_OPEN")
            if self.image_check("SIDE_SELECT_X_MENU_W"):
                print("SIDE_SELECT_X_MENU_W")
            if self.image_check("DOWN_SELECT_X_MENU_W"):
                print("DOWN_SELECT_X_MENU_W")
            if self.image_check("POKEMON_MENU_X_MENU_W"):
                print("POKEMON_MENU_X_MENU_W")
            if self.image_check("POKEMON_MENU_X_MENU_W_SELECT_SKILL"):
                print("POKEMON_MENU_X_MENU_W_SELECT_SKILL")
            if self.image_check("SKILL_PAGE_WINDOW"):
                print("SKILL_PAGE_WINDOW")
            if self.image_check("SKILL_PAGE_SIDE_SELECT_Y"):
                print("SKILL_PAGE_SIDE_SELECT_Y")
            if self.image_check("SKILL_PAGE_SIDE_SELECT_X"):
                print("SKILL_PAGE_SIDE_SELECT_X")
            if self.image_check("SKILL_PAGE_SIDE_SELECT_A"):
                print("SKILL_PAGE_SIDE_SELECT_A")
            if self.image_check("SKILL_PAGE_SIDE_SELECT_B"):
                print("SKILL_PAGE_SIDE_SELECT_B")
            self.wait(2.0)
        else:
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                self.pressRep(Button.X, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                self.wait(1.0)
            elif self.image_check("X_MENU_OPEN"):
                self.wait(1.0)
                return "COMMON_SKILL_CHANGE_POKEMON_SELECT"
            elif self.image_check("HELP_MARKER"):
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                self.wait(1.0)

        return "COMMON_SKILL_CHANGE_START_CHECK"
            
    def common_skill_change_pokemon_select(self,selectnum):
        if self.image_check("X_MENU_OPEN"):
            if self.image_check("SIDE_SELECT_X_MENU_W"):
                self.wait(0.5)
                for i in range(selectnum):
                    self.etc_sendCommand("Lbutton_right")
                    self.wait(0.5)
                self.wait(0.5)
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                self.wait(0.5)
                return "COMMON_SKILL_CHANGE_SKILL_WINDOW_OPEN"
            elif self.image_check("POKEMON_MENU_X_MENU_W"):
                for i in range(7):
                    self.etc_sendCommand("Lbutton_left")
                self.wait(0.5)
        return "COMMON_SKILL_CHANGE_POKEMON_SELECT"
    
    def common_skill_change_skill_window_open(self):
        if self.image_check("X_MENU_OPEN"):
            if self.image_check("POKEMON_MENU_X_MENU_W"):
                for i in range(2):
                    self.etc_sendCommand("Lbutton_down")
                    self.wait(0.3)
            elif self.image_check("POKEMON_MENU_X_MENU_W_SELECT_SKILL"): 
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                self.wait(0.5)
                return "COMMON_SKILL_CHANGE_SKILL_WINDOW_CHTARGET1"
        return "COMMON_SKILL_CHANGE_SKILL_WINDOW_OPEN"
        
    def common_skill_change_skill_window_chtarget1(self,target1,machine):
        if self.image_check("SKILL_PAGE_WINDOW"):
            if self.image_check("SIDE_SELECT_X_MENU_W"):
                if target1 == "X":
                    self.etc_sendCommand("Lbutton_right")
                    self.wait(0.5)
                    self.etc_sendCommand("Lbutton_up")
                elif target1 == "Y":
                    self.etc_sendCommand("Lbutton_right")
                elif target1 == "A":
                    self.etc_sendCommand("Lbutton_right")
                    self.wait(0.5)
                    self.etc_sendCommand("Lbutton_right")
                elif target1 == "B":
                    self.etc_sendCommand("Lbutton_right")
                    self.wait(0.5)
                    self.etc_sendCommand("Lbutton_down")
                else:
                    if machine==1:
                        self.pressRep(Button.ZR, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                        self.wait(0.3)
                    for i in range(target1):
                        self.etc_sendCommand("Lbutton_down")
                        self.wait(0.3)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    self.wait(0.5)
                    return "COMMON_SKILL_CHANGE_SKILL_WINDOW_CHTARGET2"
            if self.image_check("SKILL_PAGE_SIDE_SELECT_Y"):
                if target1 == "X":
                    self.etc_sendCommand("Lbutton_up")
                elif target1 == "Y":
                    self.pressRep(Button.Y, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    self.wait(0.5)
                    return "COMMON_SKILL_CHANGE_SKILL_WINDOW_CHTARGET2"
                elif target1 == "A":
                    self.etc_sendCommand("Lbutton_right")
                elif target1 == "B":
                    self.etc_sendCommand("Lbutton_down")
                #else:
                #TOPCHECKが必要なため省略
            if self.image_check("SKILL_PAGE_SIDE_SELECT_X"):
                if target1 == "X":
                    self.pressRep(Button.Y, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    self.wait(0.5)
                    return "COMMON_SKILL_CHANGE_SKILL_WINDOW_CHTARGET2"
                elif target1 == "Y":
                    self.etc_sendCommand("Lbutton_left")
                elif target1 == "A":
                    self.etc_sendCommand("Lbutton_right")
                elif target1 == "B":
                    self.etc_sendCommand("Lbutton_down")
                #else:
                #TOPCHECKが必要なため省略
            if self.image_check("SKILL_PAGE_SIDE_SELECT_A"):
                if target1 == "X":
                    self.etc_sendCommand("Lbutton_up")
                elif target1 == "Y":
                    self.etc_sendCommand("Lbutton_left")
                elif target1 == "A":
                    self.pressRep(Button.Y, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    self.wait(0.5)
                    return "COMMON_SKILL_CHANGE_SKILL_WINDOW_CHTARGET2"
                elif target1 == "B":
                    self.etc_sendCommand("Lbutton_down")
                #else:
                #TOPCHECKが必要なため省略
            if self.image_check("SKILL_PAGE_SIDE_SELECT_B"):
                if target1 == "X":
                    self.etc_sendCommand("Lbutton_up")
                elif target1 == "Y":
                    self.etc_sendCommand("Lbutton_left")
                elif target1 == "A":
                    self.etc_sendCommand("Lbutton_right")
                elif target1 == "B":
                    self.pressRep(Button.Y, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    self.wait(0.5)
                    return "COMMON_SKILL_CHANGE_SKILL_WINDOW_CHTARGET2"
                #else:
                #TOPCHECKが必要なため省略
        self.wait(0.3)
        return "COMMON_SKILL_CHANGE_SKILL_WINDOW_CHTARGET1"

    def common_skill_change_skill_window_chtarget2(self,target2):
        if self.image_check("SKILL_PAGE_WINDOW"):
            if self.image_check("SIDE_SELECT_X_MENU_W"):
                if target2 == "X":
                    self.etc_sendCommand("Lbutton_right")
                    self.wait(0.5)
                    self.etc_sendCommand("Lbutton_up")
                elif target2 == "Y":
                    self.etc_sendCommand("Lbutton_right")
                elif target2 == "A":
                    self.etc_sendCommand("Lbutton_right")
                    self.wait(0.5)
                    self.etc_sendCommand("Lbutton_right")
                elif target2 == "B":
                    self.etc_sendCommand("Lbutton_right")
                    self.wait(0.5)
                    self.etc_sendCommand("Lbutton_down")
            if self.image_check("SKILL_PAGE_SIDE_SELECT_Y"):
                if target2 == "X":
                    self.etc_sendCommand("Lbutton_up")
                elif target2 == "Y":
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    self.wait(0.5)
                    return "COMMON_SKILL_CHANGE_SKILL_WINDOW_CLOSE"
                elif target2 == "A":
                    self.etc_sendCommand("Lbutton_right")
                elif target2 == "B":
                    self.etc_sendCommand("Lbutton_down")
            if self.image_check("SKILL_PAGE_SIDE_SELECT_X"):
                if target2 == "X":
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    self.wait(0.5)
                    return "COMMON_SKILL_CHANGE_SKILL_WINDOW_CLOSE"
                elif target2 == "Y":
                    self.etc_sendCommand("Lbutton_left")
                elif target2 == "A":
                    self.etc_sendCommand("Lbutton_right")
                elif target2 == "B":
                    self.etc_sendCommand("Lbutton_down")
            if self.image_check("SKILL_PAGE_SIDE_SELECT_A"):
                if target2 == "X":
                    self.etc_sendCommand("Lbutton_up")
                elif target2 == "Y":
                    self.etc_sendCommand("Lbutton_left")
                elif target2 == "A":
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    self.wait(0.5)
                    return "COMMON_SKILL_CHANGE_SKILL_WINDOW_CLOSE"
                elif target2 == "B":
                    self.etc_sendCommand("Lbutton_down")
            if self.image_check("SKILL_PAGE_SIDE_SELECT_B"):
                if target2 == "X":
                    self.etc_sendCommand("Lbutton_up")
                elif target2 == "Y":
                    self.etc_sendCommand("Lbutton_left")
                elif target2 == "A":
                    self.etc_sendCommand("Lbutton_right")
                elif target2 == "B":
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    self.wait(0.5)
                    return "COMMON_SKILL_CHANGE_SKILL_WINDOW_CLOSE"
        self.wait(0.3)
        return "COMMON_SKILL_CHANGE_SKILL_WINDOW_CHTARGET2"
    def common_skill_change_skill_window_close(self):
        while True:
            self.pressRep(Button.B, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                return "COMMON_SKILL_CHANGE_END"
        return "COMMON_SKILL_CHANGE_SKILL_WINDOW_CLOSE"
    def common_skill_change_end(self):
        return "COMMON_SKILL_CHANGE_START"
    
    def common_skill_change_false(self):
        return "COMMON_SKILL_CHANGE_START"
    ######################################################
    # Commonboxchange
    ######################################################
    def common_box_change_function(self,target1,target2,target1_high=0,target2_high=0):
        if self.common_box_change_current_state == "COMMON_BOX_CHANGE_START":
            ret = self.common_skill_change_start()
            if ret == "COMMON_SKILL_CHANGE_START_CHECK":
                self.common_box_change_current_state = "COMMON_BOX_CHANGE_START_CHECK"
            else:
                self.common_box_change_current_state = "COMMON_BOX_CHANGE_START"
        elif self.common_box_change_current_state == "COMMON_BOX_CHANGE_START_CHECK":
            ret = self.common_skill_change_start_check()
            if ret == "COMMON_SKILL_CHANGE_POKEMON_SELECT":
                self.common_box_change_current_state = "COMMON_BOX_CHANGE_BOX_OPEN"
            else:
                self.common_box_change_current_state = "COMMON_BOX_CHANGE_START_CHECK"     
        else:
            if self.common_box_change_current_state == "COMMON_BOX_CHANGE_BOX_TARGET1":
                self.common_box_change_current_state = self.common_box_change_box_target1(target1,target1_high)   
            elif self.common_box_change_current_state == "COMMON_BOX_CHANGE_BOX_TARGET2":
                self.common_box_change_current_state = self.common_box_change_box_target2(target2-target1,target2_high - target1_high)
            else:
                self.common_box_change_current_state = self.STATE_COMMON_BOX_CHANGE_FUNCTION[self.common_box_change_current_state]()

        return self.common_box_change_current_state
    
    def common_box_change_box_open(self):
        if self.image_check("X_MENU_OPEN"):
            if self.image_check("SIDE_SELECT_X_MENU_W"):
                self.wait(0.5)
                if self.image_check("SIDE_SELECT_TOP_MAP"):
                    self.wait(0.5)
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    return "COMMON_BOX_CHANGE_BOX_TARGET1"
                self.wait(0.5)
                self.etc_sendCommand("Lbutton_up")
                self.wait(0.5)
            elif self.image_check("POKEMON_MENU_X_MENU_W"):
                for i in range(7):
                    self.etc_sendCommand("Lbutton_left")
                self.wait(0.5)
        return "COMMON_BOX_CHANGE_BOX_OPEN"
    
    def common_box_change_box_target1(self,target1,target1_high=0):
        #BOX 1:1が開始点と判定させる
        if self.image_check("BOX_WINDOW"):
            self.wait(1.0)
            if target1 > 0:
                for i in range(target1):
                    self.etc_sendCommand("Lbutton_right")
                    self.wait(1.0)
            elif target1 < 0:
                for i in range(-(target1)):
                    self.etc_sendCommand("Lbutton_left")
                    self.wait(1.0)
                    
            if target1_high > 0:
                for i in range(target1_high1):
                    self.etc_sendCommand("Lbutton_down")
                    self.wait(1.0)
            elif target1_high < 0:
                for i in range(-(target1_high)):
                    self.etc_sendCommand("Lbutton_up")
                    self.wait(1.0)
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
            self.wait(1.0) 
            return "COMMON_BOX_CHANGE_BOX_TARGET1_SELECT"        
        return "COMMON_BOX_CHANGE_BOX_TARGET1"
    
    def common_box_change_box_target1_select(self):
        if self.image_check("BOX_WINDOW"):
            if self.image_check("BOX_MENU"):
                self.wait(1.0)
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                return "COMMON_BOX_CHANGE_BOX_TARGET2"
        return "COMMON_BOX_CHANGE_BOX_TARGET1_SELECT"
    
    def common_box_change_box_target2(self,target_sub,target_sub_high=0):
        if self.image_check("BOX_WINDOW"):
            self.wait(1.0)
            if target_sub > 0:
                for i in range(target_sub):
                    self.etc_sendCommand("Lbutton_right")
                    self.wait(1.0)
            elif target_sub < 0:
                for i in range(-(target_sub)):
                    self.etc_sendCommand("Lbutton_left")
                    self.wait(1.0)
                    
            if target_sub_high > 0:
                for i in range(target_sub_high):
                    self.etc_sendCommand("Lbutton_down")
                    self.wait(1.0)
            elif target_sub_high < 0:
                for i in range(-(target_sub_high)):
                    self.etc_sendCommand("Lbutton_up")
                    self.wait(1.0)
                 
            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)   
            return "COMMON_SKILL_CHANGE_SKILL_WINDOW_CLOSE"
        return "COMMON_BOX_CHANGE_BOX_TARGET2"
    
    def common_box_change_window_close(self):
        if self.image_check("BOX_WINDOW"):
            self.pressRep(Button.B, repeat=50, duration=0.15, wait=0.5, interval=0.1)
            return "COMMON_SKILL_CHANGE_END"
        return "COMMON_SKILL_CHANGE_SKILL_WINDOW_CLOSE"

    def common_skill_change_end(self):
        return "COMMON_SKILL_CHANGE_START"
    ######################################################
    # Commonitemgive
    ######################################################
    def common_item_give_function(self,selectnum,target1,target2):
        if self.common_item_give_current_state == "COMMON_ITEM_GIVE_START":
            ret = self.common_skill_change_start()
            if ret == "COMMON_SKILL_CHANGE_START_CHECK":
                self.common_item_give_current_state = "COMMON_ITEM_GIVE_START_CHECK"
            else:
                self.common_item_give_current_state = "COMMON_ITEM_GIVE_START"
        elif self.common_item_give_current_state == "COMMON_ITEM_GIVE_START_CHECK":
            ret = self.common_skill_change_start_check()
            if ret == "COMMON_SKILL_CHANGE_POKEMON_SELECT":
                self.common_item_give_current_state = "COMMON_ITEM_GIVE_POKEMON_SELECT"
            else:
                self.common_item_give_current_state = "COMMON_ITEM_GIVE_START_CHECK" 
        elif self.common_item_give_current_state == "COMMON_ITEM_GIVE_POKEMON_SELECT":
            ret = self.common_skill_change_pokemon_select(selectnum)
            if ret == "COMMON_SKILL_CHANGE_SKILL_WINDOW_OPEN":
                self.common_item_give_current_state = "COMMON_ITEM_GIVE_WINDOW_OPEN"
            else:
                self.common_item_give_current_state = "COMMON_ITEM_GIVE_POKEMON_SELECT"        
        else:
            if self.common_item_give_current_state == "COMMON_ITEM_GIVE_TARGET_SIDE":
                self.common_item_give_current_state = self.common_item_give_target_side(target1)   
            elif self.common_item_give_current_state == "COMMON_ITEM_GIVE_TARGET_HIGH":
                self.common_item_give_current_state = self.common_item_give_target_high(target2)
            else:
                self.common_item_give_current_state = self.STATE_COMMON_ITEM_GIVE_FUNCTION[self.common_item_give_current_state]()

        return self.common_item_give_current_state
    
    def common_item_give_window_open(self):
        if self.image_check("X_MENU_OPEN"):
            if self.image_check("POKEMON_MENU_X_MENU_W"):
                for i in range(2):
                    self.etc_sendCommand("Lbutton_up")
                    self.wait(0.5)
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                self.wait(0.5)
                return "COMMON_ITEM_GIVE_TARGET_SIDE"
        return "COMMON_ITEM_GIVE_WINDOW_OPEN"
    
    def common_item_give_target_side(self,target1):
        if self.image_check("ITEM_WINDOW"):
            for i in range(target1):
                self.keys.input(Button.R)
                self.wait(0.15)
                self.keys.inputEnd(Button.R)
                self.wait(0.5)
            return "COMMON_ITEM_GIVE_TARGET_HIGH"
        return "COMMON_ITEM_GIVE_TARGET_SIDE"
    
    def common_item_give_target_high(self,target2):
        if self.image_check("ITEM_WINDOW"):
            for i in range(target2):
                self.etc_sendCommand("Lbutton_down")
                self.wait(0.5)
                
            self.pressRep(Button.A, repeat=3, duration=0.15, wait=1.0, interval=1.0)
            return "COMMON_ITEM_GIVE_WINDOW_CLOSE" 
        return "COMMON_ITEM_GIVE_TARGET_HIGH"
    
    def common_item_give_window_close(self):
        self.pressRep(Button.B, repeat=50, duration=0.15, wait=0.5, interval=0.1)
        return "COMMON_ITEM_GIVE_END"
    
    def common_item_give_end(self):
        return "COMMON_ITEM_GIVE_START"
    
    ######################################################
    # Common Map
    ######################################################
    def Common_start(self):
        #dummy
        return "COMMON_MAP_OPEN"

    def Common_map_open(self,check_pic1="FALSE_RETURN",check_pic2="FALSE_RETURN",othermap="FALSE_RETURN"):
        self.map_cursor_reset=0
        self.ZL_ACTION("END")
        self.wait(0.1)#self.wait(self.SLEEPLIST[8][2])
        # 想定外の話しかけ用
        if self.image_check("TEXT_BOX"):
            self.pressRep(Button.B, repeat=5, duration=0.15, wait=0.01, interval=0.1)
            self.wait(0.1)
        if self.image_check("TEXT_BOX2"):
            self.pressRep(Button.A, repeat=5, duration=0.15, wait=0.01, interval=0.1)
            self.wait(0.1)         
        elif self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W") or self.image_check("DEAD") or self.image_check(check_pic1) or self.image_check(check_pic2):
            self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
            self.wait(0.1)
            return "COMMON_GOTO_SELECT1"
        # ステップ遷移ミス用
        elif self.image_check("MAP"):
            return "COMMON_GOTO_SELECT1"
        elif self.image_check("MAP2") or self.image_check(othermap):
            return "COMMON_GOTO_SELECT1"
        #elif self.image_check("MORNING"):  
        #    return "CHECK_TIME"
        #elif self.image_check("NIGHT"):
        #    return "CHECK_TIME"

        return "COMMON_MAP_OPEN"
    
    def Common_goto_select1(self,position,othermap="FALSE_RETURN"):
        # position:0 すべて
        # position:1 施設
        # position:2 ポケセン
        # position:3 カフェ
        # position:4 ゾーン
        # position:5 やめる
        self.wait(0.1)#self.wait(self.SLEEPLIST[7][2])
        if self.image_check("MAP2") or self.image_check(othermap):      
            self.wait(0.1)
            if self.image_check("MOVESPOT_TAB"):
                if self.map_cursor_reset==0:
                    if self.image_check("SIDE_SELECT_TOP_MAP"):
                        self.map_cursor_reset=1
                    else:
                        self.etc_sendCommand("Lbutton_left")
                    self.wait(0.5)
                    return "COMMON_GOTO_SELECT1"
                else:
                    if self.image_check("TAB_FILTER"):       
                        self.pressRep(Button.MINUS, repeat=1, duration=0.15, wait=0.01, interval=0.1)
                        
                    elif self.image_check("SELECT_ALL"):
                        # SELECT
                        for i in range(position):
                            self.etc_sendCommand("Lbutton_down")
                            #self.wait(0.1)#回数が多い場合に移動が足りない場合は必要
                            
                        self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.01, interval=0.1)
                        return "COMMON_GOTO_SELECT2"
            else:
                    self.pressRep(Button.Y, repeat=1, duration=0.15, wait=0.1, interval=0.1)
        
        # ステップ遷移ミス用
        #elif self.image_check("MORNING"):  
        #    return "CHECK_TIME"
        #elif self.image_check("NIGHT"):
        #    return "CHECK_TIME"
        elif self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W") or self.image_check("DEAD"):
            for i in range(5):
                if self.image_check("MAP2") or self.image_check(othermap):
                    return "COMMON_GOTO_SELECT1"
                self.wait(0.1)
            print("W_select1")
            self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
            self.wait(0.1)
            return "COMMON_GOTO_SELECT1"
        elif not self.image_check("MAP2"):
            # マップ開きミス用
            for i in range(5):
                if self.image_check("MAP2"):
                    return "COMMON_GOTO_SELECT1"
                self.wait(0.1)
            self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
            self.wait(0.1)
            return "COMMON_GOTO_SELECT1"
        return "COMMON_GOTO_SELECT1"
    
    def Common_goto_select2(self,positionright,positiondown,movepoint_check,othermap="FALSE_RETURN"):
        self.wait(0.1)#self.wait(self.SLEEPLIST[7][2])
        if self.image_check("MAP2") or self.image_check(othermap):        
            if self.image_check("MOVESPOT_TAB"):         
                if self.image_check("TAB_FILTER"):
                    # FILTER
                    for i in range(positionright):
                        self.etc_sendCommand("Lbutton_right")
                        self.wait(0.1)#回数が多い場合に移動が足りない場合は必要
                    if positiondown > -1:
                        for i in range(positiondown):
                            self.etc_sendCommand("Lbutton_down")
                            self.wait(0.1)#回数が多い場合に移動が足りない場合は必要
                    else:
                        for i in range(positiondown*-1):
                            self.etc_sendCommand("Lbutton_up")
                            self.wait(0.1)#回数が多い場合に移動が足りない場合は必要
                    if movepoint_check == 0:
                        ret = self.Common_goto_jump()#移動
                        return ret
                    else:
                        return "COMMON_GOTO_JUMP"
                        
        return "COMMON_GOTO_SELECT2"

    def Common_goto_jump(self):
        self.wait(0.1)#self.wait(self.SLEEPLIST[7][2])
     
        self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.1, interval=0.1)
        for i in range(1,10):
            self.wait(0.1)#self.wait(self.SLEEPLIST[10][2])
            if self.image_check("MOVE_COMMENT"): 
                self.pressRep(Button.A, repeat=15, duration=0.15, wait=0.1, interval=0.1)
                self.sleepcount=0
                return "COMMON_CHANGE_TIME"
            
            elif self.image_check("MOVE_COMMENT_BATTLE"):
                self.inactioncount+=1
                self.pressRep(Button.B, repeat=10, duration=0.15, wait=0.1, interval=0.1)
                self.battle_step_return=1
                return "COMMON_BATTLE_RETURN"
            
            elif i == 1:
                if self.image_check("MOVE_COMMENT"): 
                    self.pressRep(Button.A, repeat=15, duration=0.15, wait=0.1, interval=0.1)
                    self.sleepcount=0
                    return "COMMON_CHANGE_TIME"
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.2, interval=0.1)
        print("MOVE_COM_ELSE")
        if self.battlecheck == 1:
            self.inactioncount+=1
            self.pressRep(Button.B, repeat=20, duration=0.15, wait=0.1, interval=0.1)
            self.battle_step_return=1
            return "COMMON_BATTLE_RETURN"
        self.sleepcount=0
        self.pressRep(Button.A, repeat=5, duration=0.15, wait=0.1, interval=0.1)
        return "COMMON_CHANGE_TIME"


    def Benchi(self):
        if self.sleepcount==0:
            self.press(Direction(Stick.LEFT, 180), duration=0.7, wait=0.1)
            self.press(Direction(Stick.LEFT, 90), duration=0.5, wait=0.1)
        else:
            self.press(Direction(Stick.LEFT, 270), duration=0.5, wait=0.1)
        self.pressRep(Button.A, repeat=12, duration=0.15, wait=0.2, interval=0.3)
        
    def Common_change_time(self):
        
        #マップコメントの捕捉失敗用
        #if self.image_check("ESCAPE"):
        #    self.battlecheck=1
        #    return "GOTO_SELECT1"
               
        #ポケモンセンター用
        #elif self.image_check("DEAD"):
        #    self.press(Direction(Stick.LEFT, 90), duration=2.0, wait=0.1)
        #    self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.2, interval=0.1)
        #    self.pressRep(Button.B, repeat=50, duration=0.15, wait=0.2, interval=0.1)
        #    if self.chicketmaxflag == 1:
        #        self.chicketmaxflag = 2
        #        return "QUASAR_MAP_OPEN"
        #    else:
        #        return "BENCH_MAP_OPEN"
        #el
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.Benchi()
            return "COMMON_CHECK_TIME"

        else:
            self.etc_sendCommand("Lbutton_left")
            self.wait(0.1)#self.wait(self.SLEEPLIST[0][2])
        return "COMMON_CHANGE_TIME"

    def Common_check_time(self,check_timing):

        # (時間切り替わりの補足ができない？その場合は朝扱いで一度抜ける(夜だった場合再度、朝・夜の切り替えを行う))
        #必ずMORNING、NIGHT判定できる時間以上のカウント数にしてください。
          
        if self.image_check("MORNING") or (check_timing != "MORNING" and self.timecount > 200):
            print("朝")
            self.timecount=0
            while True:
                #ジャスティス会への話しかけが発生する可能性があるので、ループしてしまう場合はBボタンが必要になる場合がある                
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W") or self.image_check("DEAD"):
                    self.timecount=0
                    self.changetimecount+=1
                    if check_timing != "MORNING":
                        self.sleepcount=1
                        return "COMMON_CHANGE_TIME"
                    else:
                        return "COMMON_START"

        elif self.image_check("NIGHT") or (check_timing != "NIGHT" and self.timecount > 200):
            #1ループの戦闘中移動失敗カウンタの初期化
            self.inactioncount=0
            print("夜")
            while True:
                #ジャスティス会への話しかけが発生する可能性があるので、ループしてしまう場合はBボタンが必要になる場合がある       
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W") or self.image_check("DEAD"):
                    self.timecount=0
                    self.changetimecount+=1
                    if check_timing != "NIGHT":
                        self.sleepcount=1
                        return "COMMON_CHANGE_TIME"
                    else:
                        return "COMMON_START"

        self.wait(0.1)#self.wait(self.SLEEPLIST[6][2])
        #抜けミス用カウント
        self.timecount+=1
        return "COMMON_CHECK_TIME"
    
    def Common_change_time_set(self,check_timing,type=0):
        #type=0:ポケセンブルーにて実施(バトルゾーンに影響あり)
        if self.Common_current_state == "COMMON_CHECK_TIME":  
            self.Common_current_state = self.Common_check_time(check_timing)
        elif self.Common_current_state == "COMMON_CHANGE_TIME":  
            self.Common_current_state = self.Common_change_time()
        else:
            ret = self.Common_goto(2,0,1)
            
            if ret == "START":
                self.Common_current_state = "COMMON_CHANGE_TIME"
                
        if self.Common_current_state == "COMMON_START":
            return "START"
        else:
            return "EXEC"


    def Common_goto(self,position1,position2left,position2down,movepoint_check=0,check_pic1="FALSE_RETURN",check_pic2="FALSE_RETURN",othermap="FALSE_RETURN"):
        #type=0:ポケセンブルーにて実施(バトルゾーンに影響あり)
        if self.Common_current_state == "COMMON_MAP_OPEN":
            self.Common_current_state = self.Common_map_open(check_pic1=check_pic1,check_pic2=check_pic2,othermap=othermap)
        elif self.Common_current_state == "COMMON_GOTO_SELECT1":
            self.Common_current_state = self.Common_goto_select1(position1,othermap=othermap)
        elif self.Common_current_state == "COMMON_GOTO_SELECT2":
            self.Common_current_state = self.Common_goto_select2(position2left,position2down,movepoint_check,othermap=othermap)
        else:
            self.Common_current_state = self.STATE_COMMON_FUNCTION[self.Common_current_state]()
            
        if movepoint_check==1 and self.Common_current_state == "COMMON_GOTO_JUMP":#移動先画像チェック用
            self.Common_current_state = "COMMON_START"#画像位置で停止するが、移動するかは確定出ないためstartに戻す。(移動の際は移動関数を直接叩く)
            return "MOVEPOINT_PIC"
        elif ((self.Common_current_state == "COMMON_CHANGE_TIME") or (self.Common_current_state == "COMMON_CHECK_TIME")):
            self.Common_current_state = "COMMON_START"
            return "START"
        else:
            return "EXEC"
        
    def Common_pokemon_recovery(self):  
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            self.press(Direction(Stick.LEFT, 90), duration=2.0, wait=0.1)
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.2, interval=0.1)
            if self.renda_button(rendabutton="B",endpicture="FIELD_W",endpicture2="FIELD_BACK_W",sub_button="A",sub_picture="TEXT_BLACK_COMMENT",sub2_button="A",sub2_picture="HELP_MARKER"):
                return True
        else:
            return False
    
    def Common_mappic_check(self,pic1="NULL",pic2="NULL"):
        for i in range(1,10):
            if ((pic1=="NULL" or self.image_check(pic1)) and (pic2=="NULL" or self.image_check(pic2))):
                return True
            self.wait(0.1)
        return False
    
######################################################
# ZA_battle_infi_Base
######################################################
    ######################################################
    # BENCH FUNCTION
    ###################################################### 
    def bench_start(self):
        return "BENCH_MAP_OPEN"
    
    def bench_map_open(self):
        self.ZL_ACTION("END")
        self.wait(self.SLEEPLIST[8][2])
        
        # 想定外の話しかけ用
        if self.image_check("TEXT_BOX"):
            self.pressRep(Button.B, repeat=5, duration=0.15, wait=0.01, interval=0.1)
            self.wait(0.1)
        if self.image_check("TEXT_BOX2"):
            self.pressRep(Button.A, repeat=5, duration=0.15, wait=0.01, interval=0.1)
            self.wait(0.1)        
        #マップコメントの捕捉失敗用
        if self.image_check("ESCAPE"):
            self.battlecheck=1
            self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
            return "BENCH_POKECENTER_SELECT1"   
        elif self.image_check("FIELD") or self.image_check("FIELD_BACK") or self.image_check("DEAD"):

            #マップコメントの捕捉失敗用
            if self.image_check("ESCAPE"):
                self.battlecheck=1
            else:
                self.battlecheck=0
            self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
            self.wait(0.1)
            return "BENCH_POKECENTER_SELECT1"
        # ステップ遷移ミス用
        elif self.image_check("MAP"):
            return "BENCH_POKECENTER_SELECT1"
        elif self.image_check("MORNING"):  
            return "BENCH_CHECK_TIME"
        elif self.image_check("NIGHT"):
            return "BENCH_CHECK_TIME"
        
        #バトルタイムアウト用
        elif self.image_check("ESCAPE"):
            self.battlecheck=1
            self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
            return "BENCH_POKECENTER_SELECT1"

        #はしごでマップ開けていない用
        
        elif self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):
            noescapeflg=0
            for i in range(1,20):
                if self.image_check("ESCAPE"):
                    noescapeflg=1
                    break
                elif self.image_check("SELECT"):
                    self.etc_sendCommand("Lbutton_up")
                    noescapeflg=1
                    break
                self.wait(0.1)
            
            if noescapeflg==0 and self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):
                self.MOVE_SEE("END")
                self.ZL_ACTION("END")
                self.press(Direction(Stick.LEFT, 90), duration=10.0, wait=0.1)

                self.wait(0.3)
                
                self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                self.battlecount=self.battlecount+1
                return "BENCH_POKECENTER_SELECT1"
        
        elif not (self.image_check("FIELD") or self.image_check("FIELD_BACK") or self.image_check("DEAD")):
            self.etc_sendCommand("Lbutton_left")
            #話しかけた時用のキャンセル
            self.pressRep(Button.B, repeat=1, duration=0.15, wait=0.2, interval=0.1)
            self.wait(self.SLEEPLIST[0][2])
            #戦闘中、マップを開けない状態用
            #if self.image_check("BATTLE"):
            #    if self.image_check("ESCAPE"):
            #        self.battlecheck=1
            #        self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
            #        return "BENCH_POKECENTER_SELECT1"
            #    else:
            #        self.press(Direction(Stick.LEFT, 90), duration=4.0, wait=0.01)
            #        return "BENCH_MAP_OPEN"
            
        return "BENCH_MAP_OPEN"
    
    def bench_goto_pokecenter1(self):        
        self.wait(self.SLEEPLIST[7][2])
        
        if self.image_check("MOVE_COMMENT_BATTLE"): 
            self.inactioncount+=1
            self.pressRep(Button.B, repeat=20, duration=0.15, wait=0.1, interval=0.1)
            self.battle_step_return=1
            return "BATTLE_RETURN"
        if self.image_check("MAP2"):      
            self.wait(0.1)
            if self.image_check("MOVESPOT_TAB"):         
                if self.image_check("TAB_FILTER"):       
                    self.pressRep(Button.MINUS, repeat=1, duration=0.15, wait=0.01, interval=0.1)
                    
                elif self.image_check("SELECT_ALL"):        
                    self.etc_sendCommand("Lbutton_down")
                    self.etc_sendCommand("Lbutton_down")
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.01, interval=0.1)
                    return "BENCH_POKECENTER_SELECT2"
            else:
                    self.pressRep(Button.Y, repeat=1, duration=0.15, wait=0.1, interval=0.1)
        
        # ステップ遷移ミス用
        elif self.image_check("MORNING"):  
            return "BENCH_CHECK_TIME"
        elif self.image_check("NIGHT"):
            return "BENCH_CHECK_TIME"
        elif self.image_check("FIELD") or self.image_check("FIELD_BACK") or self.image_check("DEAD"):
            return "BENCH_MAP_OPEN"
        elif not self.image_check("MAP2"):
            # マップ開きミス用
            self.wait(1.0)
            if not self.image_check("MAP2"):
                self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
        return "BENCH_POKECENTER_SELECT1"
    
    def bench_goto_pokecenter2(self):
        self.wait(self.SLEEPLIST[7][2])
        if self.image_check("MAP2"):        
            if self.image_check("MOVESPOT_TAB"):         
                if self.image_check("TAB_FILTER"):
                    self.etc_sendCommand("Lbutton_down")
                    self.etc_sendCommand("Lbutton_down")
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.1, interval=0.1)
                    for i in range(1,10):
                        self.wait(self.SLEEPLIST[10][2])
                        if self.image_check("MOVE_COMMENT"): 
                            self.pressRep(Button.A, repeat=5, duration=0.15, wait=0.1, interval=0.1)
                            self.sleepcount=0
                            return "BENCH_CHANGE_TIME"
                        elif self.image_check("MOVE_COMMENT_BATTLE"):
                            self.inactioncount+=1
                            self.pressRep(Button.B, repeat=10, duration=0.15, wait=0.1, interval=0.1)
                            self.battle_step_return=1
                            return "BATTLE_RETURN"
                        elif i == 1:
                            if self.image_check("MOVE_COMMENT"): 
                                self.pressRep(Button.A, repeat=5, duration=0.15, wait=0.1, interval=0.1)
                                self.sleepcount=0
                                return "BENCH_CHANGE_TIME"
                            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.2, interval=0.1)
                    print("MOVE_COM_ELSE")
                    if self.battlecheck == 1:
                        self.inactioncount+=1
                        self.pressRep(Button.B, repeat=20, duration=0.15, wait=0.1, interval=0.1)
                        self.battle_step_return=1
                        return "BATTLE_RETURN"
                    
                    self.pressRep(Button.A, repeat=5, duration=0.15, wait=0.1, interval=0.1)
                    return "BENCH_CHANGE_TIME"
        return "BENCH_POKECENTER_SELECT2"

    def bench_change_time(self):
        
        #マップコメントの捕捉失敗用
        if self.image_check("ESCAPE"):
            self.battlecheck=1
            return "BENCH_POKECENTER_SELECT1"
        
        if not (self.image_check("FIELD") or self.image_check("FIELD_BACK") or self.image_check("DEAD")):
            self.etc_sendCommand("Lbutton_left")
            #話しかけた時用のキャンセル
            self.pressRep(Button.B, repeat=1, duration=0.15, wait=0.2, interval=0.1)
            self.wait(self.SLEEPLIST[0][2])
            return "BENCH_CHANGE_TIME"
       
        elif self.image_check("DEAD") or self.chicketmaxflag == 1:
            self.press(Direction(Stick.LEFT, 90), duration=2.0, wait=0.1)
            self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.2, interval=0.1)
            self.pressRep(Button.B, repeat=50, duration=0.15, wait=0.2, interval=0.1)
            if self.chicketmaxflag == 1:
                self.chicketmaxflag = 2
                return "QUASAR_MAP_OPEN"
            else:
                return "BENCH_MAP_OPEN"
        elif self.image_check("FIELD") or self.image_check("FIELD_BACK"):
            self.Benchi()
            return "BENCH_CHECK_TIME"

        else:
            self.etc_sendCommand("Lbutton_left")
            self.wait(self.SLEEPLIST[0][2])
        return "BENCH_CHANGE_TIME"

    def bench_check_time(self):

        # (時間切り替わりの補足ができない？その場合は朝扱いで一度抜ける(夜だった場合再度、朝・夜の切り替えを行う))
        #必ずMORNING、NIGHT判定できる時間以上のカウント数にしてください。
        if self.timecount > 100:
        
            self.changetimemisscount+=1
        if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W") or self.image_check("DEAD"):
            return "BENCH_START"
        elif self.image_check("MORNING") or self.timecount > 100:
            print("朝")
            self.sleepcount=1
            self.timecount=0
            while True:
                #ジャスティス会への話しかけが発生する可能性があるので、ループしてしまう場合はBボタンが必要になる場合がある                
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                # 画像認識のずれで処理前に抜ける可能性があるので削除
                #if not self.image_check("MORNING") or self.timecount > 150:
                #    self.timecount=0
                #    return "BENCH_CHANGE_TIME"
                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W") or self.image_check("DEAD"):
                    self.timecount=0
                    self.changetimecount+=1
                    return "BENCH_CHANGE_TIME"
                #抜けミス用カウント
                #self.timecount+=1
        elif self.image_check("NIGHT"):
            #1ループの戦闘中移動失敗カウンタの初期化
            self.inactioncount=0
            print("夜")
            while True:
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                # 画像認識のずれで処理前に抜ける可能性があるので削除
                #if not self.image_check("NIGHT"):#解決後完全に削除 or self.timecount > 150:
                #    self.timecount=0
                #    return "BENCH_START"
                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W") or self.image_check("DEAD"):
                    self.timecount=0
                    self.changetimecount+=1
                    return "BENCH_START"
                #抜けミス用カウント
                #self.timecount+=1
        
        self.wait(self.SLEEPLIST[6][2])
        #抜けミス用カウント
        self.timecount+=1
        return "BENCH_CHECK_TIME"

    def quasar_map_open(self):
        
        ret = self.bench_map_open()
        if ret == "BENCH_POKECENTER_SELECT1":
            return "QUASAR_SELECT1"    
        else:
            return "QUASAR_MAP_OPEN"

    def goto_quasar1(self):
        self.wait(self.SLEEPLIST[7][2])
        if self.image_check("MAP2"):      
            if self.image_check("MOVESPOT_TAB"):         
                if self.image_check("TAB_FILTER"):       
                    self.pressRep(Button.MINUS, repeat=1, duration=0.15, wait=0.01, interval=0.1)
                elif self.image_check("SELECT_ALL"):        
                    self.etc_sendCommand("Lbutton_down")
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.01, interval=0.1)
                    return "QUASAR_SELECT2"
            else:
                    self.pressRep(Button.Y, repeat=1, duration=0.15, wait=0.1, interval=0.1)
        
        # ステップ遷移ミス用    
        elif self.image_check("FIELD") or self.image_check("FIELD_BACK") or self.image_check("DEAD"):
            return "QUASAR_MAP_OPEN"
        elif not self.image_check("MAP2"):
            # マップ開きミス用
            self.wait(1.0)
            if not self.image_check("MAP2"):
                self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
        return "QUASAR_SELECT1"
    
    def goto_quasar2(self):
        self.wait(self.SLEEPLIST[7][2])
        if self.image_check("MAP2"):        
            if self.image_check("MOVESPOT_TAB"):         
                if self.image_check("TAB_FILTER"):
                    self.etc_sendCommand("Lbutton_right")
                    self.wait(self.SLEEPLIST[1][2])
                    self.etc_sendCommand("Lbutton_down")
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.2, interval=0.1)
                    for i in range(1,10):
                        self.wait(self.SLEEPLIST[10][2])
                        if self.image_check("MOVE_COMMENT"): 
                            self.pressRep(Button.A, repeat=5, duration=0.15, wait=0.1, interval=0.1)
                            self.sleepcount=0
                            return "BENCH_START"
                        elif i == 1:
                            if self.image_check("MOVE_COMMENT"): 
                                self.pressRep(Button.A, repeat=5, duration=0.15, wait=0.1, interval=0.1)
                                self.sleepcount=0
                                return "BENCH_START"
                            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.2, interval=0.1)
                    print("MOVE_COM_ELSE_Q")
                    if self.battlecheck == 1:
                        self.inactioncount+=1
                        self.pressRep(Button.B, repeat=20, duration=0.15, wait=0.1, interval=0.1)
                        self.battle_step_return=1
                        return "BENCH_START"

                    self.pressRep(Button.A, repeat=5, duration=0.15, wait=0.1, interval=0.1)
                    self.sleepcount=0
                    if self.battlecount> (self.battle_zone_loop_num - 1):
                        return "BENCH_START"
                    else:
                        self.battle_step_return=0
                        return "BENCH_START"
                            
        return "QUASAR_SELECT2"
    
    def battle_return(self):
        return "BATTLE_RETURN"
    ######################################################
    # BATTLE FUNCTION
    ###################################################### 
    def battle_start(self):
        self.battlecount=0
        return "BATTLE_MAP_OPEN"
    
    def battle_map_open(self):
        self.wait(self.SLEEPLIST[8][2])
        
        if self.image_check("MORNING"):
            print("朝_loop battle_map_open")
            while True:
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                if self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W") or self.image_check("DEAD"):
                    break
            self.MOVE_SEE("END")
            self.ZL_ACTION("END")

            self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
            self.battlecount=3
            return "BATTLE_START" 
        
        if self.image_check("LOSE"):
            for i in range(20):
                self.press(Button.B, wait=0.0)
            self.quasarcount += 1
            self.quasarlosecount += 1
            self.MOVE_SEE("END")
            self.ZL_ACTION("END")
            if self.quasar_current_state=="QUASAR_BATTLE_LOOP": 
                return "QUASAR_START"
            else:
                return "BATTLE_START"
        # 想定外の話しかけ用
        if self.image_check("TEXT_BOX"):
            self.pressRep(Button.B, repeat=5, duration=0.15, wait=0.01, interval=0.1)
            self.wait(0.1)
        if self.image_check("TEXT_BOX2"):
            self.pressRep(Button.A, repeat=5, duration=0.15, wait=0.01, interval=0.1)
            self.wait(0.1)    
        
        if self.image_check("ESCAPE"):
            return "BATTLE_MOVE"
        elif self.image_check("MAP"):
            return "BATTLE_GOTO_BATTLE_ZONE1"
        elif self.image_check("DEAD"):
            return "BATTLE_START"
        elif self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
            #マップコメントの捕捉失敗用
            if self.image_check("ESCAPE"):
                return "BATTLE_MOVE"
            else:
                self.battlecheck=0
            self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
            return "BATTLE_GOTO_BATTLE_ZONE1"
        elif not(self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W")):
            for i in range(20):
                if (self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W")):
                     return "BATTLE_MAP_OPEN"
                self.wait(1.0)
            self.press(Direction(Stick.LEFT, 90), duration=6.0, wait=0.1)
            self.wait(0.3)
            self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
            return "BATTLE_MAP_OPEN"
        else:
            self.etc_sendCommand("Lbutton_left")
            self.wait(self.SLEEPLIST[0][2])
        return "BATTLE_MAP_OPEN"

    def battle_goto_battle_zone1(self):
        self.wait(self.SLEEPLIST[7][2])

        if self.image_check("MAP2"):      
            if self.image_check("MOVESPOT_TAB"):         
                if self.image_check("TAB_FILTER"):       
                    self.pressRep(Button.MINUS, repeat=1, duration=0.15, wait=0.01, interval=0.1)
                elif self.image_check("SELECT_ALL"):        
                    self.etc_sendCommand("Lbutton_down")
                    self.etc_sendCommand("Lbutton_down")
                    self.etc_sendCommand("Lbutton_down")
                    self.etc_sendCommand("Lbutton_down")
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.01, interval=0.1)
                    return "BATTLE_GOTO_BATTLE_ZONE2"
            else:
                    self.pressRep(Button.Y, repeat=1, duration=0.15, wait=0.1, interval=0.1)
        
        # ステップ遷移ミス用            
        elif self.image_check("FIELD") or self.image_check("FIELD_BACK") or self.image_check("DEAD"):
            return "BATTLE_MAP_OPEN"
        elif not self.image_check("MAP2"):
            # マップ開きミス用
            self.wait(1.0)
            if not self.image_check("MAP2"):
                self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
        return "BATTLE_GOTO_BATTLE_ZONE1"
    
    def battle_goto_battle_zone2(self):
        self.wait(self.SLEEPLIST[7][2])
        if self.image_check("MAP2"):        
            if self.image_check("MOVESPOT_TAB"):         
                if self.image_check("TAB_FILTER"):
                    for i in range(0,(self.battlecount + 1)):
                        self.etc_sendCommand("Lbutton_up")
                        
                    for i in range(0,self.battle_zone_loop_num):
                        if not self.battlecount > (self.battle_zone_loop_num - 1):
                            self.targetzone=self.zone_check()
                        if self.battlecount > (self.battle_zone_loop_num - 1):
                            break
                        elif (self.testcode==0 and(not self.ZONELIST[self.targetzone][2]) or (self.testcode==2 and (not (self.targetzone == self.testtarget)))):
                            print(str(self.targetzone) + ": " + self.ZONELIST[self.targetzone][1])
                            self.battlecount=self.battlecount+1
                            self.etc_sendCommand("Lbutton_up")
                            self.zonemisscount[self.targetzone-1]+=1
                            print("SKIP")
                            print("==================================")
                            self.wait(self.SLEEPLIST[1][2])
                        else:
                            print(str(self.targetzone) + ": " + self.ZONELIST[self.targetzone][1])
                            break
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.1, interval=0.1)

                    for i in range(1,10):
                        self.wait(self.SLEEPLIST[10][2])
                        if self.image_check("MOVE_COMMENT"): 
                            self.pressRep(Button.A, repeat=5, duration=0.15, wait=0.1, interval=0.1)
                            self.sleepcount=0

                            if self.battlecount> (self.battle_zone_loop_num - 1):
                                return "BATTLE_START"
                            else:
                                self.battle_step_return=0
                                return "BATTLE_MOVE"
                        elif self.image_check("MOVE_COMMENT_BATTLE"):
                            self.inactioncount+=1
                            self.pressRep(Button.B, repeat=10, duration=0.15, wait=0.1, interval=0.1)
                            self.battle_step_return=1
                            return "BATTLE_MOVE"
                        elif i == 1:
                            if self.image_check("MOVE_COMMENT"): 
                                self.pressRep(Button.A, repeat=5, duration=0.15, wait=0.1, interval=0.1)
                                self.sleepcount=0
                                if self.battlecount> (self.battle_zone_loop_num - 1):
                                    return "BATTLE_START"
                                else:
                                    self.battle_step_return=0
                                    return "BATTLE_MOVE"
                            self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.2, interval=0.1)
                            
                    print("MOVE_COM_ELSE")
                    if self.battlecheck == 1:
                        self.inactioncount+=1
                        self.pressRep(Button.B, repeat=20, duration=0.15, wait=0.1, interval=0.1)
                        self.battle_step_return=1
                        return "BATTLE_MOVE"

                    self.pressRep(Button.A, repeat=5, duration=0.15, wait=0.1, interval=0.1)
                    self.sleepcount=0
                    if self.battlecount> (self.battle_zone_loop_num - 1):
                        return "BATTLE_START"
                    else:
                        self.battle_step_return=0
                        return "BATTLE_MOVE"
        return "BATTLE_GOTO_BATTLE_ZONE2"
    
    def battle_move(self):
        
        if self.battle_step_return == 0:
            self.battle_step=0
        else:
        	self.battle_step=self.battle_step_return  
        
        count=0
        if self.battle_step_return == 0:
            if not (self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W")):
                for i in range(20):
                    if (self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W")):
                        return "BATTLE_MOVE"
                    self.wait(1.0)
                return "BATTLE_START"

            elif not (self.image_check("FIELD") or self.image_check("FIELD_BACK")):
                self.etc_sendCommand("Lbutton_left")
                if self.battle_current_state=="BATTLE_MOVE":
                    self.pressRep(Button.B, repeat=10, duration=0.15, wait=0.1, interval=0.1)
                if self.image_check("DEAD"):
                    return "BATTLE_START"
                elif not self.image_check("BATTLE"):
                    return "BATTLE_MOVE"
                #else:
                #    return "BATTLE_MOVE"
            elif self.image_check("DEAD"):
                return "BATTLE_START"
         
		#TEST
        if self.battle_step_return == 0:
            return self.battle_move_test()
        else:
            self.battle_step_return = 0
            return self.battle_move_test(1)      
        
    def battle_move_test(self,fast=0):
        self.quasar_battle_lockon=0
        count=0
        movestep=0
        Seecheckflg=0
        Seecheckflg2=0
        self.notargetcount=0
        self.see_r=self.SEE_DEFAULT
        
        self.MOVE_SEE("END")
        self.ZL_ACTION("END")
        
        if self.battle_current_state=="BATTLE_MOVE" and self.inactioncount>3 and self.image_check("ESCAPE"):
            self.MOVE_SEE("END")
            self.ZL_ACTION("END")

            self.battleescapecount+=1
            self.pressRep(Button.MINUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
            for loop in range(100):
                if self.image_check("ESCAPE_SELECT"):
                    self.press(Button.A, wait=0.0)
                elif self.image_check("ESCAPE_COMMENT1"):
                    self.press(Button.A, wait=0.0)
                elif self.image_check("ESCAPE_COMMENT2"):
                    for i in range(1,10):
                        self.press(Button.B, wait=0.0)
                        return "BATTLE_START"
                #補足できなかった場合の代用
                elif self.image_check("FIELD") or self.image_check("FIELD_BACK") or self.image_check("DEAD"):
                    for i in range(1,10):
                        self.press(Button.B, wait=0.0)
                        return "BATTLE_START"

        if self.ZONELIST[self.targetzone][4] == -1 or self.quasar_current_state=="QUASAR_BATTLE_LOOP":
            lockonflg = 1
        else:
            lockonflg = 0
        
        start = time.perf_counter()  # 計測開始
        end = start
        endbk = end
        lastescape = time.perf_counter() 
        
        if self.quasar_current_state=="QUASAR_BATTLE_LOOP":
            self.battle_step=1
            self.ZL_ACTION("END")
            self.ZL_ACTION("")
        else:
            if fast==0:
                #ワイルドゾーンIN
                self.press(Direction(Stick.LEFT, 90), duration=1.8, wait=0.01)
                for i in range(0,3):
                    self.press(Button.A, wait=0.0)
                self.battle_step=0
            #バトルゾーン入った直後に停止する＿
            #else:
            #    self.battle_step=1
            #    self.ZL_ACTION("END")
            #    self.ZL_ACTION("")
        
        while True:
            self.out_str = (
                f'----------------------------'
                f'\n STATE_MAIN_FUNCTION   :: {self.main_current_state}'
                f'\n'
                f'\n STATE_BENCH_FUNCTION  :: {self.bench_current_state}'
                f'\n STATE_BATTLE_FUNCTION :: {self.battle_current_state}'
                f'\n STATE_QUASAR_FUNCTION :: {self.quasar_current_state}'
                f'\n battlecount::{self.battlecount}'
                f'\n battle_step::{self.battle_step}'      
                f'\n chicketmaxflag::{self.chicketmaxflag}'
                f'\n ZL_state::{self.ZL_state}'  
                f'\n'  
                f'\n ZONECOUNT'
                f'\n[ 1 :{self.zonemisscount[0]}/{self.zonecount[0]}] '
                f'[ 2 :{self.zonemisscount[1]}/{self.zonecount[1]}] '
                f'[ 3 :{self.zonemisscount[2]}/{self.zonecount[2]}] '
                f'[ 4 :{self.zonemisscount[3]}/{self.zonecount[3]}] '
                f'[ 5 :{self.zonemisscount[4]}/{self.zonecount[4]}] '
                f'[ 6 :{self.zonemisscount[5]}/{self.zonecount[5]}] '
                f'\n[ 7 :{self.zonemisscount[6]}/{self.zonecount[6]}] '
                f'[ 8 :{self.zonemisscount[7]}/{self.zonecount[7]}] '
                f'[ 9 :{self.zonemisscount[8]}/{self.zonecount[8]}] '
                f'[10 :{self.zonemisscount[9]}/{self.zonecount[9]}] '
                f'[11 :{self.zonemisscount[10]}/{self.zonecount[10]}] '
                f'[12 :{self.zonemisscount[11]}/{self.zonecount[11]}]'
                f'\n'  
                f'\n QUASAR_LOSE_COUNT::{self.quasarlosecount}/{self.quasarcount}'
                f'\n battle_escape_count::{self.battleescapecount}'
                f'\n inactioncount::{self.inactioncount}'
                f'\n timechangemiss_count::{self.changetimemisscount}/{self.changetimecount}'
                f'\n'
                f' target_maker low:{self.target_end_low_count}/{self.target_start_low_count} mid:{self.target_end_mid_count}/{self.target_start_mid_count} normal:{self.target_end_count}/{self.target_start_count}\n'
                f' quasar_target_maker low:{self.quasar_target_end_low_count}/{self.quasar_target_start_low_count} mid:{self.quasar_target_end_mid_count}/{self.quasar_target_start_mid_count} normal:{self.quasar_target_end_count}/{self.quasar_target_start_count}\n'
                f' quasar_battle_display :{self.quasar_battle_display_end_count}/{self.quasar_battle_display_start_count}\n'
                f' battlemarker_skipcount {self.battlemarker_skipcount}/{self.battlemarker_skipcount_threshold}\n'
                f'\n'
                f'以下はTESTCODE=1でチェック {self.TESTADDCODE} ※PythonCommandBaseの編集が必要なため0とすること\n'  
                f'--------[ 50][ 55][ 60][ 65][ 70][ 75][ 80][ 85][ 90][ 95][100]\n'
                f'[left ::'
                f'[{self.target_left_max_val_list[0]:03d}]'
                f'[{self.target_left_max_val_list[1]:03d}]'
                f'[{self.target_left_max_val_list[2]:03d}]'
                f'[{self.target_left_max_val_list[3]:03d}]'
                f'[{self.target_left_max_val_list[4]:03d}]'
                f'[{self.target_left_max_val_list[5]:03d}]'
                f'[{self.target_left_max_val_list[6]:03d}]'
                f'[{self.target_left_max_val_list[7]:03d}]'
                f'[{self.target_left_max_val_list[8]:03d}]'
                f'[{self.target_left_max_val_list[9]:03d}]'
                f'[{self.target_left_max_val_list[10]:03d}]'
                f']\n'
                f'[right::'
                f'[{self.target_right_max_val_list[0]:03d}]'
                f'[{self.target_right_max_val_list[1]:03d}]'
                f'[{self.target_right_max_val_list[2]:03d}]'
                f'[{self.target_right_max_val_list[3]:03d}]'
                f'[{self.target_right_max_val_list[4]:03d}]'
                f'[{self.target_right_max_val_list[5]:03d}]'
                f'[{self.target_right_max_val_list[6]:03d}]'
                f'[{self.target_right_max_val_list[7]:03d}]'
                f'[{self.target_right_max_val_list[8]:03d}]'
                f'[{self.target_right_max_val_list[9]:03d}]'
                f'[{self.target_right_max_val_list[10]:03d}]'
                f']\n'
                f'\n----------------------------'
                )
            self.print_tb("d"); self.print_t(f'{self.out_str}')
            
            #バトルゾーンで朝になった場合
            if self.image_check("MORNING") and self.battle_current_state=="BATTLE_MOVE":
                print("朝_BATTLE_LOOP")

                self.wait(0.3)
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                #リザルト判定の取得ミスのため、ミスカウントはしない
                #self.zonemisscount[self.targetzone-1]+=1
                self.MOVE_SEE("END")
                self.ZL_ACTION("END")
                #マップコメントの捕捉失敗用
                self.wait(0.3)
                
                self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                self.battlecount=self.battlecount+1
                return "BATTLE_START"
            #はしごなどで逃げるボタン非活性の場合、はしごにのぼる
            
            
            if self.battle_current_state=="BATTLE_MOVE" and self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):
                print("check1")
                noescapeflg=0
                for i in range(1,self.escapecheckrange):
                    if self.image_check("ESCAPE"):
                        noescapeflg=1
                        break
                    elif self.image_check("SELECT"):
                        self.etc_sendCommand("Lbutton_up")
                        noescapeflg=1
                        break
                    self.wait(0.1)
                
                if noescapeflg==0 and self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):
                    self.MOVE_SEE("END")
                    self.ZL_ACTION("END")
                    self.press(Direction(Stick.LEFT, 90), duration=10.0, wait=0.1)

                    self.wait(0.3)
                    
                    self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                    self.battlecount=self.battlecount+1
                    return "BATTLE_START"
            #バトルゾーン話しかけ対応(ひとまずひたすらAで再度話しかけを許容して、その後話しかけをBで終了(アイテムはＡボタンでないと進めないため))
            if self.battle_current_state=="BATTLE_MOVE" and (self.image_check("TEXT_BOX") or self.image_check("TEXT_BOX2")):
                self.MOVE_SEE("END")
                self.ZL_ACTION("END")
                self.pressRep(Button.A, repeat=20, duration=0.15, wait=0.1, interval=0.1)
                self.pressRep(Button.B, repeat=20, duration=0.15, wait=0.1, interval=0.1)

            #敗北用の保険                
            if self.battle_current_state=="BATTLE_MOVE" and self.image_check("LOSE"):
                self.wait(1.0)
                self.pressRep(Button.A, repeat=10, duration=0.15, wait=0.01, interval=0.1)
                self.pressRep(Button.B, repeat=30, duration=0.15, wait=0.01, interval=0.1)
                return "BATTLE_START"

            if self.battle_step==0 and self.battle_current_state=="BATTLE_MOVE":
                self.etc_sendCommand("Lbutton_up")
            # 想定外の話しかけ用
            if self.image_check("TEXT_BOX"):
                if self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.image_check("REWORD_END"):
                    for i in range(5):
                        self.press(Button.B, wait=0.0)
                    self.quasarcount += 1
                    self.MOVE_SEE("END")
                    self.ZL_ACTION("END")
                    return "QUASAR_START"
                elif self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.image_check("REWORD_LOSE"):
                    for i in range(5):
                        self.press(Button.B, wait=0.0)
                    self.quasarcount += 1
                    self.quasarlosecount += 1
                    self.MOVE_SEE("END")
                    self.ZL_ACTION("END")
                    return "QUASAR_START"
                else:
                    self.wait(1.0)#判定できない場合待機してから再度確認
                    if self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.image_check("REWORD_END"):
                        for i in range(5):
                            self.press(Button.B, wait=0.0)
                        self.quasarcount += 1
                        self.MOVE_SEE("END")
                        self.ZL_ACTION("END")
                        return "QUASAR_START"
                    elif self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.image_check("REWORD_LOSE"):
                        for i in range(5):
                            self.press(Button.B, wait=0.0)
                        self.quasarcount += 1
                        self.quasarlosecount += 1
                        self.MOVE_SEE("END")
                        self.ZL_ACTION("END")
                        return "QUASAR_START"
                    self.pressRep(Button.B, repeat=1, duration=0.15, wait=0.05, interval=0.1)
                    self.wait(0.1)
            #アイテムテキスト用
            if self.image_check("TEXT_BOX2"):#基本的にこちらに入る場合、報酬ありなので問題なし
                if self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.image_check("REWORD_END"):
                    for i in range(5):
                        self.press(Button.B, wait=0.0)
                    self.quasarcount += 1
                    self.MOVE_SEE("END")
                    self.ZL_ACTION("END")
                    return "QUASAR_START"
                elif self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.image_check("REWORD_LOSE"):
                    for i in range(5):
                        self.press(Button.B, wait=0.0)
                    self.quasarcount += 1
                    self.quasarlosecount += 1
                    self.MOVE_SEE("END")
                    self.ZL_ACTION("END")
                    return "QUASAR_START"
                else:
                    self.wait(1.0)#判定できない場合待機してから再度確認
                    if self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.image_check("REWORD_END"):
                        for i in range(5):
                            self.press(Button.B, wait=0.0)
                        self.quasarcount += 1
                        self.MOVE_SEE("END")
                        self.ZL_ACTION("END")
                        return "QUASAR_START"
                    elif self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.image_check("REWORD_LOSE"):
                        for i in range(5):
                            self.press(Button.B, wait=0.0)
                        self.quasarcount += 1
                        self.quasarlosecount += 1
                        self.MOVE_SEE("END")
                        self.ZL_ACTION("END")
                        return "QUASAR_START"
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.05, interval=0.1)
                    self.wait(0.1)        
			#バトル中はチェックしない
            if self.battle_current_state=="BATTLE_MOVE" and self.battle_step != 1 and self.image_check("CHICKET_MAX_RIGHT"):
                print("CHICKET_MAX2")
                self.chicketmaxflag = 1
                self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                self.battlecount=3
                return "BATTLE_START"   
            if self.battle_current_state=="BATTLE_MOVE" and self.image_check("MORNING"):
                print("朝_loop")
                for i in range(100):
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.5, interval=0.1)
                    if self.image_check("FIELD") or self.image_check("FIELD_BACK") or self.image_check("DEAD"):
                        break
                self.MOVE_SEE("END")
                self.ZL_ACTION("END")

                if self.image_check("ESCAPE"):
                    self.battlecheck=1
                    self.battle_nofiled_count=0
                    break
                elif self.battle_current_state=="BATTLE_MOVE" and self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):
                    self.battlecheck=1
                    print("check2")
                    noescapeflg=0
                    for i in range(1,self.escapecheckrange):
                        if self.image_check("ESCAPE"):
                            noescapeflg=1
                            break
                        elif self.image_check("SELECT"):
                            self.etc_sendCommand("Lbutton_up")
                            noescapeflg=1
                            break
                        self.wait(0.1)
                    
                    if noescapeflg==0 and self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):
                        self.MOVE_SEE("END")
                        self.ZL_ACTION("END")
                        self.press(Direction(Stick.LEFT, 90), duration=10.0, wait=0.1)

                        self.wait(0.3)
                        
                        self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                        self.battlecount=self.battlecount+1
                        return "BATTLE_START"
                
                else:
                    self.battlecheck=0
                    break
                self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                self.battlecount=3
                return "BATTLE_START"             
                

            ### バトル終了の抜けミス対策
            if self.battle_step==1 and self.battle_current_state=="BATTLE_MOVE":
                noescapetime = time.perf_counter()
                escapeelapsed = noescapetime - lastescape
                if escapeelapsed >= 30:
                    print("エスケープマークが30.0秒以上経過しました。強制的に終了します。")
                    #リザルト判定の取得ミスのため、ミスカウントはしない
                    #self.zonemisscount[self.targetzone-1]+=1
                    self.MOVE_SEE("END")
                    self.ZL_ACTION("END")
                    #マップコメントの捕捉失敗用

                    if self.image_check("ESCAPE"):
                        self.battlecheck=1
                        self.battle_nofiled_count=0
                        break
                    elif self.battle_current_state=="BATTLE_MOVE" and self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):
                        self.battlecheck=1
                        print("check3")
                        noescapeflg=0
                        for i in range(1,self.escapecheckrange):
                            if self.image_check("ESCAPE"):
                                noescapeflg=1
                                break
                            elif self.image_check("SELECT"):
                                self.etc_sendCommand("Lbutton_up")
                                noescapeflg=1
                                break
                            self.wait(0.1)
                        
                        if noescapeflg==0 and self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):
                            self.MOVE_SEE("END")
                            self.ZL_ACTION("END")
                            self.press(Direction(Stick.LEFT, 90), duration=10.0, wait=0.1)

                            self.wait(0.3)
                            
                            self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                            self.battlecount=self.battlecount+1
                            return "BATTLE_MAP_OPEN"

                    else:
                        self.battlecheck=0
                        break
                    
                    # コメントなどの場合用のキャンセル
                    for i in range(1,20):
                        self.press(Button.B, wait=0.0)
                    self.wait(0.1)
                    
                    self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                    self.battlecount=self.battlecount+1
                    return "BATTLE_MAP_OPEN"
                    
            self.ZL_ACTION(lockonflg=lockonflg)
            if self.ZL_state == 1:
                for i in range(5):
                    # 技使用を判定させるため
                    if self.no_Cplus==0 and self.image_check("C+"):
                        self.notarget_movecount=0
                        self.press(Button.A, wait=0.0)
                        self.press(Button.B, wait=0.0)
                        self.notargetcount=0
                    elif self.no_Cplus==1:#C+がない場合の処理
                        self.press(Button.A, wait=0.0)
                        self.press(Button.B, wait=0.0)
                        self.press(Button.X, wait=0.0)
                    ### リワード戦コメント送り or カード拾いなど
                    elif self.quasar_current_state=="QUASAR_BATTLE_LOOP" or (self.battle_step==0 and self.battle_current_state=="BATTLE_MOVE"):
                        self.press(Button.A, wait=0.0)

                    if self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.image_check("REWORD_END"):
                        for i in range(5):
                            self.press(Button.B, wait=0.0)
                        self.quasarcount += 1
                        self.MOVE_SEE("END")
                        self.ZL_ACTION("END")
                        return "QUASAR_START"
                    elif self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.image_check("REWORD_LOSE"):
                        for i in range(5):
                            self.press(Button.B, wait=0.0)
                        self.quasarcount += 1
                        self.quasarlosecount += 1
                        self.MOVE_SEE("END")
                        self.ZL_ACTION("END")
                        return "QUASAR_START"
                if self.no_Cplus==0 and self.image_check("C+"):
                    self.press(Button.A, wait=0.0)
                    self.press(Button.B, wait=0.0)
                    self.notargetcount=0
                    if not self.image_check("ESCAPE"):
                        self.notargetcount=0
                elif self.no_Cplus==1:#C+がない場合の処理
                    self.press(Button.A, wait=0.0)
                    self.press(Button.B, wait=0.0)
                    self.press(Button.X, wait=0.0)
                if self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.image_check("REWORD_END"):
                    for i in range(5):
                        self.press(Button.B, wait=0.0)
                    self.quasarcount += 1
                    self.MOVE_SEE("END")
                    self.ZL_ACTION("END")
                    return "QUASAR_START"
                elif self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.image_check("REWORD_LOSE"):
                    for i in range(5):
                        self.press(Button.B, wait=0.0)
                    self.quasarcount += 1
                    self.quasarlosecount += 1
                    self.MOVE_SEE("END")
                    self.ZL_ACTION("END")
                    return "QUASAR_START"
                if self.no_Cplus==0 and self.image_check("C+"):
                    self.press(Button.X, wait=0.0)
                    self.notargetcount=0
                elif self.no_Cplus==1:#C+がない場合の処理
                    self.press(Button.A, wait=0.0)
                    self.press(Button.B, wait=0.0)
                    self.press(Button.X, wait=0.0)
                    if not self.image_check("ESCAPE"):
                        self.notargetcount=0
                
            if self.battle_current_state=="BATTLE_MOVE" and self.image_check("EYE_CHECK_HIGH"):
                Seecheckflg+=1
                if Seecheckflg>7 or (((movestep - 1) == self.ZONELIST[self.targetzone][3]) and Seecheckflg2 == 2):
                    self.MOVE_SEE()
                    #self.press(Direction(Stick.RIGHT, 90), duration=0.03, wait=0.1)
                elif Seecheckflg>5 and (self.no_Cplus==0 and self.image_check("C+")) or (((movestep - 1) == self.ZONELIST[self.targetzone][3]) and (Seecheckflg2 == 1 and (self.no_Cplus==0 and self.image_check("C+")))):
                    self.MOVE_SEE("END")
                    Seecheckflg2=2
                elif Seecheckflg>5 and ((self.no_Cplus==0 and (not self.image_check("C+")))) or (((movestep - 1) == self.ZONELIST[self.targetzone][3]) and Seecheckflg2 == 0 and ((self.no_Cplus==0 and (not self.image_check("C+"))))):
                    self.MOVE_SEE()

            elif self.battle_current_state=="BATTLE_MOVE" and (self.ZONELIST[self.targetzone][5 + movestep][3] and self.image_check("EYE_CHECK")):
                Seecheckflg+=1
                if Seecheckflg>7 or (((movestep - 1) == self.ZONELIST[self.targetzone][3]) and Seecheckflg2 == 2):
                    self.MOVE_SEE()
                    #self.press(Direction(Stick.RIGHT, 90), duration=0.03, wait=0.1)
                elif Seecheckflg>5 and (self.no_Cplus==0 and self.image_check("C+")) or (((movestep - 1) == self.ZONELIST[self.targetzone][3]) and (Seecheckflg2 == 1 and (self.no_Cplus==0 and self.image_check("C+")))):
                    self.MOVE_SEE("END")
                    Seecheckflg2=2
                elif Seecheckflg>5 and ((self.no_Cplus==0 and (not self.image_check("C+")))) or (((movestep - 1) == self.ZONELIST[self.targetzone][3]) and Seecheckflg2 == 0 and ((self.no_Cplus==0 and (not self.image_check("C+"))))):
                    self.MOVE_SEE()
                    
            elif self.battle_current_state=="BATTLE_MOVE" and (not (self.ZONELIST[self.targetzone][5 + movestep][3] and self.image_check("EYE_CHECK"))): 
                self.MOVE_SEE("END")
                Seecheckflg=0

            #敗北用の保険                
            if self.battle_current_state=="BATTLE_MOVE" and self.image_check("LOSE"):
                self.wait(1.0)
                self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.01, interval=0.1)
                self.pressRep(Button.B, repeat=5, duration=0.15, wait=0.01, interval=0.1)
                return "BATTLE_START"
                
            if (self.battle_step==1 and self.battle_current_state=="BATTLE_MOVE" and self.image_check("REWARD_RESULT")) or self.battle_step==2:
                lastescape = time.perf_counter() 
                endbk = end
                end = time.perf_counter()
                self.DebugLog(2,"while if REWARD_RESULT",end,endbk)
                
                self.battle_step=2
                for i in range(1,15):
                    self.pressRep(Button.A, repeat=1, duration=0.15, wait=0.01, interval=0.1)
                    if (self.image_check("CHICKET_MAX") or self.image_check("CHICKET_MAX_RIGHT"))and self.chicketmaxflag == 0:
                        print("CHICKET_MAX")
                        self.battlecount=3
                        self.chicketmaxflag = 1
                    
                self.battlecount=self.battlecount+1
                
                end = time.perf_counter()    # 計測終了
                print(f"処理時間: {end - start:.5f} 秒")
                print("==================================")
                self.notargetcount=0
                
                if self.battlecount>(self.battle_zone_loop_num - 1):
                    self.battle_step=0
                    self.MOVE_SEE("END")
                    self.ZL_ACTION("END")
                    return "BATTLE_START"
                self.battle_step=0
                self.MOVE_SEE("END")
                self.ZL_ACTION("END")
                return "BATTLE_MAP_OPEN"
            
            elif self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.image_check("REWORD_END"):
                for i in range(5):
                    self.press(Button.B, wait=0.0)
                self.quasarcount += 1
                self.MOVE_SEE("END")
                self.ZL_ACTION("END")
                return "QUASAR_START"
            elif self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.image_check("REWORD_LOSE"):
                for i in range(5):
                    self.press(Button.B, wait=0.0)
                self.quasarcount += 1
                self.quasarlosecount += 1
                self.MOVE_SEE("END")
                self.ZL_ACTION("END")
                return "QUASAR_START"
    
            elif self.image_check("ESCAPE") or self.image_check("BATTLE_BALL_CHECK"):
                
                endbk = end
                end = time.perf_counter()
                self.DebugLog(3,"while elif ESCAPE",end,endbk)
                
                if self.battle_step==0:
                    
                    endbk = end
                    end = time.perf_counter()
                    self.DebugLog(4,"while elif ESCAPE step0",end,endbk)
                    
                    #end = time.perf_counter()    # 計測途中
                    print(f"バトル開始時間: {end - start:.5f} 秒")
                    self.battle_step=1
                    self.notargetcount=0
                    lockonflg=1
                self.ZL_ACTION("END")
                self.ZL_ACTION("")

                self.battle_lockon_test()
                   
                if self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.image_check("REWORD_END"):
                    for i in range(5):
                        self.press(Button.B, wait=0.0)
                    self.quasarcount += 1
                    self.MOVE_SEE("END")
                    self.ZL_ACTION("END")
                    return "QUASAR_START"
                elif self.quasar_current_state=="QUASAR_BATTLE_LOOP" and self.image_check("REWORD_LOSE"):
                    for i in range(5):
                        self.press(Button.B, wait=0.0)
                    self.quasarcount += 1
                    self.quasarlosecount += 1
                    self.MOVE_SEE("END")
                    self.ZL_ACTION("END")
                    return "QUASAR_START"
                   
                    
                if self.battle_step==1:
                    if ((not self.image_check("ESCAPE")) and (self.no_Cplus==0 and (not self.image_check("C+"))) and (self.image_check("BATTLE_BALL_CHECK"))and self.battle_current_state=="BATTLE_MOVE"):

                        self.battlecheck=1
                        print("check4")
                        noescapeflg=0
                        for i in range(1,self.escapecheckrange):
                            if self.image_check("ESCAPE"):
                                noescapeflg=1
                                break
                            elif self.image_check("SELECT"):
                                self.etc_sendCommand("Lbutton_up")
                                noescapeflg=1
                                break
                            self.wait(0.1)
                        
                        if noescapeflg==0 and self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):
                            self.MOVE_SEE("END")
                            self.ZL_ACTION("END")
                            self.press(Direction(Stick.LEFT, 90), duration=10.0, wait=0.1)

                            self.wait(0.3)
                            
                            self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                            self.battlecount=self.battlecount+1
                            return "BATTLE_MAP_OPEN"             
                    
                    lockonflg = 1
                    lastescape = time.perf_counter() 
                    endbk = end
                    end = time.perf_counter()
                    elapsed = end - start
                    #ハマった場合の逃走(ヤミラミループなど)
                    if elapsed >= 200 and self.battle_current_state=="BATTLE_MOVE":
                        print("200.0秒以上経過しました。逃走し強制的に終了します。")
                        self.MOVE_SEE("END")
                        self.ZL_ACTION("END")
                        if self.image_check("ESCAPE"):
                            self.battleescapecount+=1
                            self.battle_nofiled_count=0
                            self.pressRep(Button.MINUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                            for i in range(100):#無限ループ抜け
                                if self.image_check("ESCAPE_SELECT"):
                                    self.press(Button.A, wait=0.0)
                                elif self.image_check("ESCAPE_COMMENT1"):
                                    self.press(Button.A, wait=0.0)
                                elif self.image_check("ESCAPE_COMMENT2"):
                                    for i in range(1,10):
                                        self.press(Button.B, wait=0.0)
                                        return "BATTLE_START"
                                #補足できなかった場合の代用
                                elif self.image_check("FIELD") or self.image_check("FIELD_BACK") or self.image_check("DEAD"):
                                    for i in range(1,10):
                                        self.press(Button.B, wait=0.0)
                                        return "BATTLE_START"
                                self.wait(0.1)
                        
                        elif self.battle_current_state=="BATTLE_MOVE" and self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):

                            print("check5")
                            noescapeflg=0
                            for i in range(1,self.escapecheckrange):
                                if self.image_check("ESCAPE"):
                                    noescapeflg=1
                                    break
                                elif self.image_check("SELECT"):
                                    self.etc_sendCommand("Lbutton_up")
                                    noescapeflg=1
                                    break
                                self.wait(0.1)
                            
                            if noescapeflg==0 and self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):
                                self.MOVE_SEE("END")
                                self.ZL_ACTION("END")
                                self.press(Direction(Stick.LEFT, 90), duration=10.0, wait=0.1)

                                self.wait(0.3)
                                
                                self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                                self.battlecount=self.battlecount+1
                                return "BATTLE_MAP_OPEN"           

                        else:
                            #マップコメントの捕捉失敗用

                            if self.image_check("ESCAPE"):
                                self.battlecheck=1
                                self.battle_nofiled_count=0
                                break
                            elif self.battle_current_state=="BATTLE_MOVE" and self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):
                                print("check6")
                                noescapeflg=0
                                for i in range(1,self.escapecheckrange):
                                    if self.image_check("ESCAPE"):
                                        noescapeflg=1
                                        break
                                    elif self.image_check("SELECT"):
                                        self.etc_sendCommand("Lbutton_up")
                                        noescapeflg=1
                                        break
                                    self.wait(0.1)
                                
                                if noescapeflg==0 and self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):
                                    self.MOVE_SEE("END")
                                    self.ZL_ACTION("END")
                                    self.press(Direction(Stick.LEFT, 90), duration=10.0, wait=0.1)

                                    self.wait(0.3)
                                    
                                    self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                                    self.battlecount=self.battlecount+1
                                    return "BATTLE_MAP_OPEN"
                            else:

                                self.battlecheck=0
                                break
                        self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                        self.battlecount=self.battlecount+1
                        return "BATTLE_MAP_OPEN"    

                    self.DebugLog(5,"while elif ESCAPE step1",end,endbk)
                    
                    if self.image_check("SELECT"):

                        endbk = end
                        end = time.perf_counter()
                        self.DebugLog(6,"while elif ESCAPE step1 SELECT",end,endbk)
                        for i in range(0,3):
                            self.etc_sendCommand("Lbutton_up")
                    elif (self.no_Cplus==0 and self.image_check("C+")):
                        self.notargetcount=0
                        self.MOVE_SEE("END")
                    elif not self.image_check("ESCAPE"):
                        self.notargetcount=0
                        self.MOVE_SEE("END")
                    else:
                        if self.notargetcount > 8:
                            self.ZL_ACTION(lockonflg=lockonflg)
                            self.MOVE_SEE()
                        #ハマり対策仮
                        #if notargetcount % 2 == 1:
                        #    self.MOVE_SEE("END")
                        #    self.ZL_ACTION("END")
                        #    self.wait(0.1)
                        #    self.ZL_ACTION()
                        #    self.MOVE_SEE()
                        if self.notargetcount % 10 == 9:
                            if self.battle_current_state=="BATTLE_MOVE":
                                self.press(Direction(Stick.LEFT, 90), duration=0.3, wait=0.1)
                            else:
                                #リワードロック対策での移動距離を多めにする。
                                self.MOVE_SEE("END")
                                self.ZL_ACTION("END")
                                self.press(Direction(Stick.LEFT, 90), duration=3.0, wait=0.1)
                                self.ZL_ACTION()
                                self.MOVE_SEE()
                                
                            self.notarget_movecount+=1
                            if self.notarget_movecount>3:
                                #逃げ
                                self.MOVE_SEE("END")
                                self.ZL_ACTION("END")
                                if self.image_check("ESCAPE"):
                                    self.battleescapecount+=1
                                    self.battle_nofiled_count=0
                                    self.pressRep(Button.MINUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                                    for i in range(100):
                                        if self.image_check("ESCAPE_SELECT"):
                                            self.press(Button.A, wait=0.0)
                                        elif self.image_check("ESCAPE_COMMENT1"):
                                            self.press(Button.A, wait=0.0)
                                        elif self.image_check("ESCAPE_COMMENT2"):
                                            for i in range(1,10):
                                                self.press(Button.B, wait=0.0)
                                                return "BATTLE_START"
                                        #補足できなかった場合の代用
                                        elif self.image_check("FIELD") or self.image_check("FIELD_BACK") or self.image_check("DEAD"):
                                            for i in range(1,10):
                                                self.press(Button.B, wait=0.0)
                                                return "BATTLE_START"
                                        self.wait(0.1)
                                elif self.battle_current_state=="BATTLE_MOVE" and self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):
                                    print("check7")
                                    noescapeflg=0
                                    for i in range(1,self.escapecheckrange):
                                        if self.image_check("ESCAPE"):
                                            noescapeflg=1
                                            break
                                        elif self.image_check("SELECT"):
                                            self.etc_sendCommand("Lbutton_up")
                                            noescapeflg=1
                                            break
                                        self.wait(0.1)
                                    
                                    if noescapeflg==0 and self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):
                                        self.MOVE_SEE("END")
                                        self.ZL_ACTION("END")
                                        self.press(Direction(Stick.LEFT, 90), duration=10.0, wait=0.1)

                                        self.wait(0.3)
                                        
                                        self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                                        self.battlecount=self.battlecount+1
                                        return "BATTLE_MAP_OPEN"
                                
                                else:
                                    #マップコメントの捕捉失敗用

                                    if self.image_check("ESCAPE"):
                                        self.battlecheck=1
                                        self.battle_nofiled_count=0
                                        break
                                    elif self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):
                                        self.battlecheck=1
                                        print("check8")
                                        noescapeflg=0
                                        for i in range(1,self.escapecheckrange):
                                            if self.image_check("ESCAPE"):
                                                noescapeflg=1
                                                break
                                            elif self.image_check("SELECT"):
                                                self.etc_sendCommand("Lbutton_up")
                                                noescapeflg=1
                                                break
                                            self.wait(0.1)
                                        
                                        if noescapeflg==0 and self.image_check("BATTLE_BALL_CHECK") and (not self.image_check("ESCAPE")):
                                            self.MOVE_SEE("END")
                                            self.ZL_ACTION("END")
                                            self.press(Direction(Stick.LEFT, 90), duration=10.0, wait=0.1)

                                            self.wait(0.3)
                                            
                                            self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                                            self.battlecount=self.battlecount+1
                                            return "BATTLE_MAP_OPEN"
                                    else:

                                        self.battlecheck=0
                                        break
                                self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                                self.battlecount=self.battlecount+1
                                return "BATTLE_MAP_OPEN"
                        
            else:
                if self.battle_step==0 and self.battle_current_state=="BATTLE_MOVE":
                    if count > self.ZONELIST[self.targetzone][4]:
                        lockonflg=1
                    self.etc_sendCommand("Lbutton_up")
                    if Seecheckflg==0:
                        movestep = self.MOVE_ACTION(movestep,lockonflg=lockonflg)
                    #movestep=+1
                    end = time.perf_counter()
                    elapsed = end - start

                    if elapsed >= 40 and self.battle_current_state=="BATTLE_MOVE":
                        print("40.0秒以上経過しました。強制的に終了します。")
                        self.battlecount=self.battlecount+1
                        self.zonemisscount[self.targetzone-1]+=1
                        self.MOVE_SEE("END")
                        self.ZL_ACTION("END")
                        #マップコメントの捕捉失敗用

                        if self.image_check("ESCAPE"):
                            self.battlecheck=1
                            self.battle_nofiled_count=0
                            break
                        else:

                            self.battlecheck=0
                            break
                        # コメントなどの場合用のキャンセル
                        for i in range(1,20):
                            self.press(Button.B, wait=0.0)
                        self.wait(0.1)
                            
                        self.pressRep(Button.PLUS, repeat=1, duration=0.15, wait=0.3, interval=0.1)
                        self.battlecount=self.battlecount+1
                        return "BATTLE_MAP_OPEN"
                    self.notargetcount=0

            self.checkIfAlive()
            count=count+1
            self.notargetcount += 1

        self.MOVE_SEE("END")
        self.ZL_ACTION("END")

        return "BATTLE_MAP_OPEN" 

    def battle_lockon_test(self):
        self.quasar_battle_lockon=1
        self.battlemarker_skipcount=self.battlemarker_skipcount_threshold
        self.notargetcount=0
        start = time.perf_counter()  # 計測開始
        while True:
            if self.notargetcount>3:
                if (self.battle_current_state=="BATTLE_MOVE" and (self.notargetcount % 9 == 1)):
                    self.press(Direction(Stick.LEFT, 90), duration=0.9, wait=0.1)
                elif (self.battle_current_state=="QUASAR_BATTLE_LOOP" and (self.notargetcount % 9 == 1)):
                    self.press(Direction(Stick.LEFT, 90), duration=0.9, wait=0.1)
                self.MOVE_SEE("")
            self.ZL_ACTION("END")
            self.ZL_ACTION("")
            #self.press(Button.A, wait=0.0)
            end = time.perf_counter()
            elapsed = end - start
            

            if self.image_check("R_push"):
                self.press(Button.RCLICK,0.05,0.1) 

            if (self.no_Cplus==0 and self.image_check("C+")):
                self.MOVE_SEE("END")
                self.press(Button.A, wait=0.0)
                self.press(Button.B, wait=0.0)
                self.notargetcount=0
                return
            elif self.no_Cplus==1:#C+がない場合の処理
                self.press(Button.A, wait=0.0)
                self.press(Button.B, wait=0.0)
                self.press(Button.X, wait=0.0)
            
            elif self.battle_step==1 and self.battle_current_state=="BATTLE_MOVE" and self.image_check("REWARD_RESULT"):
                self.battle_step=2
                self.MOVE_SEE("END")
                return
            elif self.battle_current_state=="BATTLE_MOVE" and self.image_check("LOSE"):
                self.MOVE_SEE("END")
                return
            
            if (self.image_check("REWORD_END") or self.image_check("REWORD_LOSE")):
                self.MOVE_SEE("END")
                return
            if self.image_check("SELECT"):
                self.MOVE_SEE("END")
                return
            if not self.image_check("ESCAPE"):
                self.MOVE_SEE("END")
                return
            
            if self.image_check("ESCAPE") or self.image_check("FIELD_W") or self.image_check("FIELD_BACK_W"):
                #if self.image_check("TARGET_L_ALL"):
                self.battlemarker_skipcount+=1
                if ((self.battlemarker_skipcount > self.battlemarker_skipcount_threshold) and (self.image_check("TARGET_RIGHT_LOW") or self.image_check("TARGET_LEFT_LOW") or (self.Rstick_state == 0 and (self.image_check("TARGET_RIGHT_RIHGT_CHECK_LOW") or self.image_check("TARGET_LEFT_RIHGT_CHECK_LOW"))))):# LOWで数回確認後通常のマーカーでもチェックできた場合継続(画像検知位置は回転を考慮し左寄り) 視点回転していない場合右も確認

                
                    self.MOVE_SEE("END")
                    if self.quasar_current_state=="QUASAR_BATTLE_LOOP":
                        self.quasar_target_start_low_count+=1
                    else:
                        self.target_start_low_count+=1
                    time.sleep(0.2)
                    for i in range(0,3):
                       #print("target_loop")

                        if (self.no_Cplus==0 and self.image_check("C+")):
                            self.notargetcount=0
                            self.press(Button.A, wait=0.0)
                            self.press(Button.B, wait=0.0)
                            #print("##### target_loop_END")
                            if self.quasar_current_state=="QUASAR_BATTLE_LOOP":
                                self.quasar_target_end_low_count+=1
                            else:
                                self.target_end_low_count+=1
                            return
                        elif self.no_Cplus==1:#C+がない場合の処理
                            self.press(Button.A, wait=0.0)
                            self.press(Button.B, wait=0.0)
                            self.press(Button.X, wait=0.0)
                        elif self.image_check("SELECT"):
                            if self.quasar_current_state=="QUASAR_BATTLE_LOOP":
                                self.quasar_target_start_low_count+=1
                            else:
                                self.target_start_low_count-=1
                            return
                        elif not self.image_check("ESCAPE"):
                            if self.quasar_current_state=="QUASAR_BATTLE_LOOP":
                                self.quasar_target_start_low_count+=1
                            else:
                                self.target_start_low_count-=1
                            return
                        
                        if not self.image_check("ESCAPE"):
                            self.notargetcount=0
                            
                        self.ZL_ACTION("END")
                        time.sleep(0.2)
                        self.ZL_ACTION("")
                        time.sleep(0.2)
                        #self.notargetcount=0#
                        
                    if self.image_check("TARGET_RIGHT") or self.image_check("TARGET_LEFT") or (self.Rstick_state == 0 and (self.image_check("TARGET_RIGHT_RIHGT_CHECK") or self.image_check("TARGET_LEFT_RIHGT_CHECK"))):# 視点回転していない場合右も確認
                        if self.quasar_current_state=="QUASAR_BATTLE_LOOP":
                            self.quasar_target_start_mid_count+=1
                        else:
                            self.target_start_mid_count+=1
                        if (self.no_Cplus==0 and self.image_check("C+")):
                            self.notargetcount=0
                            self.press(Button.A, wait=0.0)
                            self.press(Button.B, wait=0.0)
                            #print("##### target_loop_END")
                            if self.quasar_current_state=="QUASAR_BATTLE_LOOP":
                                self.quasar_target_end_mid_count+=1
                            else:
                                self.target_end_mid_count+=1
                            return
                        elif self.no_Cplus==1:#C+がない場合の処理
                            self.press(Button.A, wait=0.0)
                            self.press(Button.B, wait=0.0)
                            self.press(Button.X, wait=0.0)
                        elif self.image_check("SELECT"):
                            if self.quasar_current_state=="QUASAR_BATTLE_LOOP":
                                self.quasar_target_start_mid_count-=1
                            else:
                                self.target_start_mid_count-=1
                            return
                        elif not self.image_check("ESCAPE"):
                            if self.quasar_current_state=="QUASAR_BATTLE_LOOP":
                                self.quasar_target_start_mid_count-=1
                            else:
                                self.target_start_mid_count-=1
                            return
                        
                        if not self.image_check("ESCAPE"):
                            self.notargetcount=0
                        
                        self.ZL_ACTION("END")
                        time.sleep(0.2)
                        self.ZL_ACTION("")
                        time.sleep(0.2)
                        self.notargetcount+=1
                    else:
                        #LOWでチェックできない場合、しばらくLOWでのチェックをしない(同じ画面でLOWチェックを連続しておこなわないように) 主に車のタイヤで誤チェックされてしまう
                        #if self.battle_current_state=="BATTLE_MOVE":
                            #テスト バトルエリアのみLOWモードの間隔をあける
                        self.battlemarker_skipcount=0
                        self.notargetcount+=1
                             
                    
                elif ((self.battlemarker_skipcount <= self.battlemarker_skipcount_threshold) and (self.image_check("TARGET_RIGHT") or self.image_check("TARGET_LEFT") or (self.Rstick_state == 0 and (self.image_check("TARGET_RIGHT_RIHGT_CHECK") or self.image_check("TARGET_LEFT_RIHGT_CHECK"))))):# 視点回転していない場合右も確認 LOWでチェックミスがある場合しばらくLOWを使用しない。

                    self.MOVE_SEE("END")
                    
                    if self.quasar_current_state=="QUASAR_BATTLE_LOOP":
                        self.quasar_target_start_count+=1
                    else:
                        self.target_start_count+=1
                    time.sleep(0.2)
                    for i in range(0,3):
                       #print("target_loop")

                        if (self.no_Cplus==0 and self.image_check("C+")):
                            self.notargetcount=0
                            self.press(Button.A, wait=0.0)
                            self.press(Button.B, wait=0.0)
                            #print("##### target_loop_END")
                            if self.quasar_current_state=="QUASAR_BATTLE_LOOP":
                                self.quasar_target_end_count+=1
                            else:
                                self.target_end_count+=1
                            return
                        elif self.no_Cplus==1:#C+がない場合の処理
                            self.press(Button.A, wait=0.0)
                            self.press(Button.B, wait=0.0)
                            self.press(Button.X, wait=0.0)
                        elif self.image_check("SELECT"):
                            if self.quasar_current_state=="QUASAR_BATTLE_LOOP":
                                self.quasar_target_start_count-=1
                            else:
                                self.target_start_count-=1
                            return
                        elif not self.image_check("ESCAPE"):
                            if self.quasar_current_state=="QUASAR_BATTLE_LOOP":
                                self.quasar_target_start_count-=1
                            else:
                                self.target_start_count-=1
                            return
                        
                        if not self.image_check("ESCAPE"):
                            self.notargetcount=0
                        
                        self.ZL_ACTION("END")
                        time.sleep(0.2)
                        self.ZL_ACTION("")
                        time.sleep(0.2)
                    self.notargetcount+=1
                elif ((self.quasar_current_state=="QUASAR_BATTLE_LOOP" and (self.image_check("ATTACK_DISPLAY") or self.image_check("ATTACK_C+_DISPLAY"))) or (self.Rstick_state == 0 and (self.quasar_current_state=="QUASAR_BATTLE_LOOP" and (self.image_check("ATTACK_DISPLAY_RIHGT_CHECKW") or self.image_check("ATTACK_C+_DISPLAY_RIHGT_CHECKW"))))):# 攻撃表示による判定
                #elif ( (self.image_check("ATTACK_DISPLAY") or self.image_check("ATTACK_C+_DISPLAY"))or (self.Rstick_state == 0 and (self.image_check("ATTACK_DISPLAY_RIHGT_CHECKW") or self.image_check("ATTACK_C+_DISPLAY_RIHGT_CHECKW")))):# 攻撃表示による判定
                    self.MOVE_SEE("END")
                    self.quasar_battle_display_start_count+=1
                    time.sleep(0.2)
                    for i in range(0,3):
                        if (self.no_Cplus==0 and self.image_check("C+")):
                            self.notargetcount=0
                            self.press(Button.A, wait=0.0)
                            self.press(Button.B, wait=0.0)
                            #print("##### target_loop_END")
                            self.quasar_battle_display_end_count+=1
                            return
                        elif self.no_Cplus==1:#C+がない場合の処理
                            self.press(Button.A, wait=0.0)
                            self.press(Button.B, wait=0.0)
                            self.press(Button.X, wait=0.0)
                        elif self.image_check("SELECT"):
                            self.quasar_battle_display_start_count-=1
                            return
                        elif not self.image_check("ESCAPE"):
                            self.quasar_battle_display_start_count-=1
                            return
                        
                        if not self.image_check("ESCAPE"):
                            self.notargetcount=0
                        
                        self.ZL_ACTION("END")
                        time.sleep(0.2)
                        self.ZL_ACTION("")
                        time.sleep(0.2)
                        self.notargetcount+=1
                else:
                    self.notargetcount+=1
            else:
                ## 交換中などのため0にする(間隔をあけるため-8?)
                self.MOVE_SEE("END")
                self.notargetcount=0#-8
                self.press(Button.A, wait=0.0)
                    
            if elapsed >= 20:
                return
                    
            
    def battle_lockon_test_all(self):
        if self.image_check("TARGET_LEFT"):
            print("left_check")
        
        if self.image_check("TARGET_RIGHT"):
            print("right_check")

    def DebugLog(self,num,logmessage,endtime=0,starttime=0):
        return
        if starttime == 0:
            print(f"[lognum:{num}] {logmessage}")
        else:
            print(f"[lognum:{num}] {logmessage} 処理時間: {endtime - starttime:.5f} 秒")

    ######################################################
    # QUASAR_FUNCTION
    ###################################################### 
    def quasar_start(self):
        self.chicketmaxflag = 0
        return "QUASAR_MOVE_DOOR"
    def quasar_move_door(self):
        if not (self.image_check("FIELD") or self.image_check("FIELD_BACK") or self.image_check("DEAD")):
            self.etc_sendCommand("Lbutton_left")
            self.wait(self.SLEEPLIST[0][2])
            return "QUASAR_MOVE_DOOR"
        
        self.press(Direction(Stick.LEFT, 90), duration=7.0, wait=0.1)
        if self.image_check("DOOR_A"):
            self.press(Button.A, wait=0.0)
            return "QUASAR_MOVE_ENTRANCE"
        return "QUASAR_MOVE_DOOR"
    def quasar_move_entrance(self):
        if not (self.image_check("FIELD") or self.image_check("FIELD_BACK") or self.image_check("DEAD")):
            self.etc_sendCommand("Lbutton_left")
            self.wait(self.SLEEPLIST[0][2])
            return "QUASAR_MOVE_ENTRANCE"
        
        self.press(Direction(Stick.LEFT, 90), duration=11.0, wait=0.1)
        self.press(Direction(Stick.LEFT, 10), duration=1.0, wait=0.1)
        for i in range(30):
            self.press(Button.A, wait=0.0)
        return "QUASAR_BATTLE_LOOP"
    
    def quasar_battle_loop(self):
        self.notargetcount=0
        return self.battle_move_test()

######################################################
# ZA_battle_infi_Base_End
######################################################
    
    ######################################################
    # 画像認識
    ######################################################
    def image_check(self,targetimage,nocheckflag=1):
        # テスト用出力スキップ
        if nocheckflag==0:
            return False
        
        ######################################################
        # MAIN_0_START PIC
        ######################################################
        if targetimage=="PROFILE":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\_0_Start\Profile.png',
                                    threshold = 0.8,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [60,40,260,70]
                                    ):
                
                return True
            else:
                return False
        
        elif targetimage=="STARTBTN_SELECT":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\_0_Start\startbutton_select.png',
                                    threshold = 0.8,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [120,520,500,610]
                                    ):
                return True
            else:
                return False
        ######################################################
        # 1_Z_LANK PIC
        ######################################################
        elif targetimage=="TEXT_TRAIN_OUT_COMMENT":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\_1_z_lank\station_field.png',
                                    threshold = 0.8,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [1020,120,1210,190]
                                    ):
                return True
            else:
                return False
            
        elif targetimage=="TEXT_STATION_LEAVE_COMMENT":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\_1_z_lank\station_leave_comment.png',
                                    threshold = 0.8,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [950,130,1150,230]
                                    ):
                return True
            else:
                return False

        elif targetimage=="SLEEP_ICON":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\_1_z_lank\\sleep_icon.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [300,150,900,650]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="WANINOKO_ICON":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\_1_z_lank\\waninokoicon.png',
                                        threshold = 0.80,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [50,640,350,680],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False
        elif targetimage=="QUASAR_MOVIE_ICON":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\_1_z_lank\\quasar_movie_icon.png',
                                        threshold = 0.80,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [250,150,850,550],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False
        elif targetimage=="TEXT_2_GETCHANCE":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\_1_z_lank\\getchance_comment.png',
                                    threshold = 0.9,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [300,555,1000,700]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="TEXT_2_GET_SUCCESS":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\_1_z_lank\\2get_success.png',
                                    threshold = 0.9,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [300,555,1000,700]
                                    ):
                return True
            else:
                return False
        elif targetimage=="KOHUKI_ICON_GET4":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\_1_z_lank\\kohukiicon.png',
                                        threshold = 0.75,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [200,640,250,680],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False           
        elif targetimage=="MERIP_ICON_GET5":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\_1_z_lank\\meripicon.png',
                                        threshold = 0.75,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [250,640,300,680],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False
        ######################################################
        # 2_Y_LANK PIC
        ######################################################
        elif targetimage=="PIKA_ICON_GET6":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\_2_y_lank\\pikaicon.png',
                                        threshold = 0.75,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [300,640,350,680],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False
        elif targetimage=="PIKA_ICON_BOX6":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\_2_y_lank\\pikaicon_box6.png',
                                        threshold = 0.75,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [450,80,550,200],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False
        elif targetimage=="W_BATTLE_END":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\_2_y_lank\\Wbattle_end.png',
                                        threshold = 0.85,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [50,80,200,200],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False
        ######################################################
        # 4_E_LANK PIC
        ######################################################
        elif targetimage=="ODAIRU_ICON":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\_4_e_lank\\Odairu_icon.png',
                                        threshold = 0.80,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [50,640,350,680],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False 
            
        elif targetimage=="ABSOL_ICON":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\_4_e_lank\\absol_icon.png',
                                        threshold = 0.80,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [50,640,350,680],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False 
        elif targetimage=="REIBI_SKILL":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\_4_e_lank\\reibi_skill.png',
                                        threshold = 0.80,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [40,200,320,300],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False 
            
        ######################################################
        # COMMON
        ######################################################
        elif targetimage=="TEXT_BLACK_COMMENT":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\black_comment.png',
                                    threshold = 0.9,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [300,555,1000,700]
                                    ):
                return True
            else:
                return False
        elif targetimage=="TEXT_WHITE_COMMENT":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\white_comment.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [300,555,1000,700]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="TEXT_WHITE_COMMENT2":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\white_comment2.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [300,555,1000,700]
                                    ):
                return True
            else:
                return False
        elif targetimage=="1_SELECT":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\1_select.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [920,400,1180,550]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="2_SELECT":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\2_select.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [920,400,1180,550]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="2_SELECT_TUTORIAL":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\2_select_tutorial.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [920,400,1180,550]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="3_SELECT":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\3_select.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [920,340,1180,550]
                                    ):
                return True
            else:
                return False
        elif targetimage=="3_SELECT_SELECT":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\3_select_select.png',
                                    threshold = 0.9,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [920,340,1180,550]
                                    ):
                return True
            else:
                return False
        elif targetimage=="4_SELECT":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\4_select.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [920,300,1180,550]
                                    ):
                return True
            else:
                return False
        elif targetimage=="CHAT_MARKER":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\chatmarker.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [600,300,850,500]
                                    ):
                return True
            else:
                return False
        elif targetimage=="HELP_MARKER":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\helpmarker.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [300,50,500,110]
                                    ):
                return True
            else:
                return False
        elif targetimage=="BATTLE_BALL_CHECK":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\battle_ball_check.png',
                                    threshold = 0.95,
                                    use_gray = False,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [500,30,850,70],
                                    crop_template  = []
                                    ):
                return True
            else:
                return False 
        if targetimage=="ESCAPE":
            if self.isContainTemplateUltra_get_max_val(                
                    template_path ='ZA_Story\Common\\escape.png',
                    threshold = 0.85,
                    use_gray = True,
                    show_value = False,
                    show_position = True,
                    show_only_true_rect  = False,
                    ms  = 2000,
                    crop = [54,477,75,497],
                    crop_template  = []
                    ):
                return True
            else:
                return False
        
        elif targetimage=="FIELD":
            if self.isContainTemplateUltra_get_max_val(                
                                template_path ='ZA_Story\Common\\field.png',
                                threshold = 0.80,
                                use_gray = True,
                                show_value = False,
                                show_position = True,
                                show_only_true_rect  = False,
                                ms  = 2000,
                                crop = [50,680,97,720],
                                crop_template  = []
                                ):
                return True
            else:
                return False
        elif targetimage=="FIELD_BACK":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\Common\\field_back.png',
                                        threshold = 0.80,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [50,680,97,720],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False
        elif targetimage=="FIELD_W":
            if self.isContainTemplateUltra_get_max_val(                
                                template_path ='ZA_Story\Common\\field.png',
                                threshold = 0.80,
                                use_gray = True,
                                show_value = False,
                                show_position = True,
                                show_only_true_rect  = False,
                                ms  = 2000,
                                crop = [50,680,350,720],
                                crop_template  = []
                                ):
                return True
            else:
                return False
        elif targetimage=="FIELD_BACK_W":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\Common\\field_back.png',
                                        threshold = 0.80,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [50,680,350,720],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False
        elif targetimage=="FIELD1":
            if self.isContainTemplateUltra_get_max_val(                
                                template_path ='ZA_Story\Common\\field.png',
                                threshold = 0.80,
                                use_gray = True,
                                show_value = False,
                                show_position = True,
                                show_only_true_rect  = False,
                                ms  = 2000,
                                crop = [50,680,100,720],
                                crop_template  = []
                                ):
                return True
            else:
                return False
        elif targetimage=="FIELD_BACK1":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\Common\\field_back.png',
                                        threshold = 0.80,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [50,680,100,720],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False
        elif targetimage=="FIELD2":
            if self.isContainTemplateUltra_get_max_val(                
                                template_path ='ZA_Story\Common\\field.png',
                                threshold = 0.80,
                                use_gray = True,
                                show_value = False,
                                show_position = True,
                                show_only_true_rect  = False,
                                ms  = 2000,
                                crop = [100,680,150,720],
                                crop_template  = []
                                ):
                return True
            else:
                return False
        elif targetimage=="FIELD_BACK2":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\Common\\field_back.png',
                                        threshold = 0.80,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [100,680,150,720],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False
        elif targetimage=="FIELD3":
            if self.isContainTemplateUltra_get_max_val(                
                                template_path ='ZA_Story\Common\\field.png',
                                threshold = 0.80,
                                use_gray = True,
                                show_value = False,
                                show_position = True,
                                show_only_true_rect  = False,
                                ms  = 2000,
                                crop = [150,680,200,720],
                                crop_template  = []
                                ):
                return True
            else:
                return False
        elif targetimage=="FIELD_BACK3":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\Common\\field_back.png',
                                        threshold = 0.80,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [150,680,200,720],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False

        elif targetimage=="FIELD4":
            if self.isContainTemplateUltra_get_max_val(                
                                template_path ='ZA_Story\Common\\field.png',
                                threshold = 0.80,
                                use_gray = True,
                                show_value = False,
                                show_position = True,
                                show_only_true_rect  = False,
                                ms  = 2000,
                                crop = [200,680,250,720],
                                crop_template  = []
                                ):
                return True
            else:
                return False
        elif targetimage=="FIELD_BACK4":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\Common\\field_back.png',
                                        threshold = 0.80,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [200,680,250,720],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False
        elif targetimage=="FIELD5":
            if self.isContainTemplateUltra_get_max_val(                
                                template_path ='ZA_Story\Common\\field.png',
                                threshold = 0.80,
                                use_gray = True,
                                show_value = False,
                                show_position = True,
                                show_only_true_rect  = False,
                                ms  = 2000,
                                crop = [250,680,300,720],
                                crop_template  = []
                                ):
                return True
            else:
                return False
        elif targetimage=="FIELD_BACK5":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\Common\\field_back.png',
                                        threshold = 0.80,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [250,680,300,720],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False
        elif targetimage=="FIELD6":
            if self.isContainTemplateUltra_get_max_val(                
                                template_path ='ZA_Story\Common\\field.png',
                                threshold = 0.80,
                                use_gray = True,
                                show_value = False,
                                show_position = True,
                                show_only_true_rect  = False,
                                ms  = 2000,
                                crop = [300,680,350,720],
                                crop_template  = []
                                ):
                return True
            else:
                return False
        elif targetimage=="FIELD_BACK6":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\Common\\field_back.png',
                                        threshold = 0.80,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [300,680,350,720],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False
        elif targetimage=="DEAD":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\Common\\dead.png',
                                        threshold = 0.80,
                                        use_gray = True,
                                        show_value = False,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [50,640,350,680],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False
        elif targetimage=="OUT_MARKER":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\outmarker.png',
                                    threshold = 0.80,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [600,300,850,500]
                                    ):
                return True
            else:
                return False
        elif targetimage=="IN_MARKER":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\inmarker.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [600,300,850,500]
                                    ):
                return True
            else:
                return False   
            
        elif targetimage=="IN_ICON":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\in_icon.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [300,150,900,350]
                                    ):
                return True
            else:
                return False 
           
        elif targetimage=="ELEVATOR_ICON":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\elevator_icon.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [300,150,900,600]
                                    ):
                return True
            else:
                return False 

        elif targetimage=="GETCHANCE_ICON4":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\getmerker4.png',
                                    threshold = 0.60,#75(メリープををチェックできないため)
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [300,150,1000,720]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="X_MENU_OPEN":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\X_menu\\x_menu_window.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [50,50,450,120]
                                    ):
                return True
            else:
                return False
        elif targetimage=="SIDE_SELECT_X_MENU_W":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\X_menu\\side_select.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [30,150,100,700]
                                    ):
                return True
            else:
                return False
        elif targetimage=="SIDE_SELECT_TOP_MAP":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\X_menu\\side_select.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [20,160,100,230]
                                    ):
                return True
            else:
                return False
        elif targetimage=="DOWN_SELECT_X_MENU_W":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\X_menu\\down_select.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [550,120,1250,160]
                                    ):
                return True
            else:
                return False
        elif targetimage=="POKEMON_MENU_X_MENU_W":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\X_menu\\pokemon_menu.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [550,120,1250,500]
                                    ):
                return True
            else:
                return False
        elif targetimage=="POKEMON_MENU_X_MENU_W_SELECT_SKILL":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\X_menu\\pokemon_menu_select_skill.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [550,120,1250,500]
                                    ):
                return True
            else:
                return False  
        elif targetimage=="SKILL_PAGE_WINDOW":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\X_menu\\skillpage.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [550,170,750,250]
                                    ):
                return True
            else:
                return False
        elif targetimage=="SKILL_PAGE_SIDE_SELECT_Y":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\X_menu\\side_select.png',
                                    threshold = 0.92,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [560,360,600,400]
                                    ):
                return True
            else:
                return False  
        elif targetimage=="SKILL_PAGE_SIDE_SELECT_A":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\X_menu\\side_select.png',
                                    threshold = 0.92,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [880,360,930,400]
                                    ):
                return True
            else:
                return False
        elif targetimage=="SKILL_PAGE_SIDE_SELECT_X":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\X_menu\\side_select.png',
                                    threshold = 0.92,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [720,300,760,350]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="SKILL_PAGE_SIDE_SELECT_B":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\X_menu\\side_select.png',
                                    threshold = 0.92,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [720,410,760,460]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="EVENT_MARKER_CENTER":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\event_marker.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [640,0,680,600]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="EVENT_MARKER_CENTER_WIDE":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\event_marker.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [600,0,720,600]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="EVENT_MARKER_LEFT_WIDE":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\event_marker.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [250,0,680,600]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="EVENT_MARKER_RIGHT_WIDE":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\event_marker.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [640,0,1100,600]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="HASHIGO_ICON":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\hashigomarker.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [300,150,900,650]
                                    ):
                return True
            else:
                return False
        elif targetimage=="C+":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\C+.png',
                                    threshold = 0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [1000,565,1280,720],
                                    crop_template  = []):
                return True
            else:
                #カラスバ戦の白背景で検知できないため白背景用
                if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\Common\\C+2.png',
                                        threshold = 0.75,
                                        use_gray = False,
                                        show_value = self.show_value_bool,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [1000,565,1280,720],
                                        crop_template  = []):
                    return True
                else:
                    return False
                return False
        elif targetimage=="MAP2" or targetimage=="MAP":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\map2.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [20,0,200,70],
                                    crop_template  = []
                                    ):   
                return True
            else:
                return False
        elif targetimage=="UG_SEWER_MAP":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\underground_sewer_map.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [20,0,250,70],
                                    crop_template  = []
                                    ):   
                return True
            else:
                return False
        elif targetimage=="MORNING":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\morning.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [540,155,740,350],
                                    crop_template  = []
                                    ):    
                return True
            else:
                return False
        elif targetimage=="NIGHT":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\night.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [430,350,850,520],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVE_COMMENT":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\move_comment.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [290,550,1000,690],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVESPOT_TAB":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\movespot_tab.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [30,120,220,250],
                                    crop_template  = []
                                    ):        
                return True
            else:
                return False
        elif targetimage=="SELECT_ALL":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\Common\\select_all.png',
                                        threshold = 0.75,
                                        use_gray = True,
                                        show_value = self.show_value_bool,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [20,270,280,595],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False
        elif targetimage=="TAB_FILTER":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\tab_filter.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [30,570,90,600],
                                    crop_template  = []
                                    ): 
                return True
            else:
                return False
        elif targetimage=="TEXT_BOX":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\text_box.png',
                                    threshold = 0.8,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [550,555,1000,680]
                                    ):
                return True
            else:
                return False
        elif targetimage=="TEXT_BOX2":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\text_box2.png',
                                    threshold = 0.95,#85
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [550,555,1000,680]
                                    ):
                return True
            else:
                return False
            
        elif targetimage=="TEXT_GREEN_COMMENT":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\green_comment.png',
                                    threshold = 0.9,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [300,555,1000,700]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="PIN_MARKER_CENTER":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\pin_marker.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [640,0,680,600]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="PIN_MARKER_CENTER_WIDE":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\pin_marker.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [600,0,720,600]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="PIN_MARKER_LEFT_WIDE":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\pin_marker.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [250,0,680,600]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="PIN_MARKER_RIGHT_WIDE":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\pin_marker.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [640,0,1100,600]
                                    ):
                return True
            else:
                return False
        elif targetimage=="SELECT":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\SELECT.png',
                                    threshold = 0.80,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [80,640,135,695]
                                    ):
                return True
            else:
                return False
        elif targetimage=="COIN_ICON":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\many_icon.png',
                                    threshold = 0.8,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [1000,0,1200,100]
                                    ):
                return True
            else:
                return False
        elif targetimage=="EYE_CHECK":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\eye_check.png',
                                    threshold = 0.80,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [600,50,700,120],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="EYE_CHECK_HIGH":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\eye_check_high.png',
                                    threshold = 0.80,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [400,50,900,120],
                                    crop_template  = []
                                    ):
                return True
            else:
                return False 
        elif targetimage=="EYE_CHECK_HIGH_POKE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\eye_check_high_p.png',
                                    threshold = 0.80,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [400,50,900,120],
                                    crop_template  = []
                                    ):
                return True
            else:
                return False 
        elif targetimage=="SIDE_MARKER_CENTER_WIDE":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\side_marker.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [600,0,720,600]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="SIDE_MARKER_LEFT_WIDE":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\side_marker.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [250,0,680,600]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="SIDE_MARKER_RIGHT_WIDE":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\side_marker.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [640,0,1100,600]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="SIDE_MARKER_CENTER":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\side_marker.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [640,0,680,600]
                                    ):
                return True
            else:
                return False 

        elif targetimage=="BATTLE":
            if self.isContainTemplateUltra_get_max_val(                
                                        template_path ='ZA_Story\Common\\battle.png',
                                        threshold = 0.75,
                                        use_gray = True,
                                        show_value = self.show_value_bool,
                                        show_position = True,
                                        show_only_true_rect  = False,
                                        ms  = 2000,
                                        crop = [50,640,350,680],
                                        crop_template  = []
                                        ):
                return True
            else:
                return False
        elif targetimage=="ARROW":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\arrow.png',
                                    threshold = 0.88,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [910,620,966,676],
                                    crop_template  = []
                                    ):
                return True
            else:
                return False
        elif targetimage=="ZA_ROYALE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\z-a_royale.png',
                                    threshold = 0.88,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [20,40,380,80],
                                    crop_template  = []
                                    ):
                return True
            else:
                return False
        elif targetimage=="M_BALL_ICON":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\ball_icon\\m_ball.png',
                                    threshold = 0.85,
                                    use_gray = False,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [610,595,670,650]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="H_BALL_ICON":
            if self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\Common\\ball_icon\\h_ball.png',
                                    threshold = 0.85,
                                    use_gray = False,
                                    show_value = False,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [610,595,670,650]
                                    ):
                return True
            else:
                return False 
        elif targetimage=="BOX_WINDOW":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\boxwindow.png',
                                    threshold = 0.88,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [160,10,290,60],
                                    crop_template  = []
                                    ):
                return True
            else:
                return False
        elif targetimage=="BOX_MENU":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\boxmenu.png',
                                    threshold = 0.88,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [20,40,850,700],
                                    crop_template  = []
                                    ):
                return True
            else:
                return False
        elif targetimage=="ITEM_WINDOW":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\Common\\itemwindow.png',
                                    threshold = 0.88,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [80,30,230,65],
                                    crop_template  = []
                                    ):
                return True
            else:
                return False
        #デフォルトTrueReturnで画像チェックする用
        elif targetimage=="TRUE_RETURN":
            return True
        #デフォルトFalseReturnで画像チェックする用
        elif targetimage=="FALSE_RETURN":
            return False
        ######################################################
        # COMMON MOVEPOINT_TARGET
        ######################################################
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE4":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE4_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_TARGET_POKECENTER_RUDU":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\pokecenter_rudu_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_TARGET_RESTAURANT_DREAM":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\restaurant_dream_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_TARGET_CAFE_MAN":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_man_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_TARGET_ROSE_SQUARE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\rose_square_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_TARGET_POKECENTER_ROSE_S":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\pokecenter_rose_square_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_TARGET_POKECENTER_ROSE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\pokecenter_rose_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_POKECENTER_PRANTAN":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\pokecenter_prantan_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_POKECENTER_BLUE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\pokecenter_blue_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_POKECENTER_EVEL":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\pokecenter_evel_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_CAFE_RETAKE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_retake_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_POKECENTER_JONE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\pokecenter_jone_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE2":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE2_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE5":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE5_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE6":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE6_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_CAFE_ALAMODE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_alamode_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_CAFE_TOTO":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_toto_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_CAFE_TWISTER":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_twister_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_CAFE_NUVO2":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_nuvo2_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_BLUE_SQUARE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\bule_square_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_CAFE_SOLEIL":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_soleil_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_CAFE_FOCUS":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_focus_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_CAFE_SLALOM":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_slalom_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_CAFE_NUVO3":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_nuvo3_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_CAFE_CANCODOR":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_cancodor_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_RESTAURANT_2RYU":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\restaurant_2ryu_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_ART_MUSEUM":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\art_museum_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_HOTEL_SURREALISH":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\hotel_surrealish_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_CAFE_ULT":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_ult_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_CAFE_PARTENAIRE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_partenaire_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_CAFE_BATAILLE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_bataille_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_RACINE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\racine_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_RESTAURANT_DOHUTSU":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\restaurant_dohutsu_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_JUSTICE_DOJO":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\justice_dojo_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_RESTAURANT_EXTREAME":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\restaurant_exterme_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_CAFE_CUTE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_cute_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE8":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE8_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE9":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE9_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE10":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE10_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE11":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE11_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE12":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE12_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE13":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE13_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE14":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE14_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE15":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE15_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE16":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE16_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE17":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE17_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE18":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE18_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE19":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE19_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_TARGET_W_ZONE20":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE20_target.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,450,600],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        ######################################################
        # COMMON MOVEPOINT_PIC
        ######################################################
        elif targetimage=="MOVEPOINT_PIC_W_ZONE4":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE4_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_POKECENTER_RUDU":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\pokecenter_rudu_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False     
        elif targetimage=="MOVEPOINT_PIC_RESTAURANT_DREAM":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\restaurant_dream_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False   
        elif targetimage=="MOVEPOINT_PIC_CAFE_MAN":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_man_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_ROSE_SQUARE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\rose_square_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_POKECENTER_ROSE_S":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\pokecenter_rose_square_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_POKECENTER_ROSE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\pokecenter_rose_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_POKECENTER_PRANTAN":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\pokecenter_prantan_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_POKECENTER_BLUE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\pokecenter_blue_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_POKECENTER_EVEL":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\pokecenter_evel_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_CAFE_RETAKE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_retake_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_POKECENTER_JONE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\pokecenter_jone_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_W_ZONE2":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE2_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_W_ZONE5":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE5_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_W_ZONE6":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE6_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
            
            
        elif targetimage=="MOVEPOINT_PIC_CAFE_ALAMODE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_alamode_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_CAFE_TOTO":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_toto_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_CAFE_TWISTER":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_twister_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_CAFE_NUVO2":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_nuvo2_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_BLUE_SQUARE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\bule_square_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_CAFE_FOCUS":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_focus_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_CAFE_SLALOM":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_slalom_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_CAFE_NUVO3":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_nuvo3_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_CAFE_CANCODOR":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_cancodor_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_CAFE_SOLEIL":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_soleil_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_RESTAURANT_2RYU":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\restaurant_2ryu_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_ART_MUSEUM":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\art_museum_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_HOTEL_SURREALISH":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\hotel_surrealish_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_CAFE_ULT":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_ult_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_CAFE_PARTENAIRE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_partenaire_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_CAFE_BATAILLE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_bataille_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_RACINE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\racine_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_RESTAURANT_DOHUTSU":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\restaurant_dohutsu_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_JUSTICE_DOJO":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\justice_dojo_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_RESTAURANT_EXTREAME":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\restaurant_exterme_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_CAFE_CUTE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\cafe_cute_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVEPOINT_PIC_W_ZONE8":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE8_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_W_ZONE9":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE9_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_W_ZONE10":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE10_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_W_ZONE11":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE11_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_W_ZONE12":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE12_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_W_ZONE13":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE13_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_W_ZONE14":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE14_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_W_ZONE15":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE15_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_W_ZONE16":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE16_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_W_ZONE17":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE17_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_W_ZONE18":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE18_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_W_ZONE19":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE19_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="MOVEPOINT_PIC_W_ZONE20":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\MovePoint\\W_ZONE20_pic.png',
                                    threshold = 0.90,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [850,100,1270,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        ######################################################
        # ZA_INFI
        ######################################################
        elif targetimage=="REWARD_RESULT":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\REWARD.png',
                                    threshold = 0.75,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [930,45,1030,60],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="CHICKET_MAX":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\chicket_max.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [700,600,1000,750],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="CHICKET_MAX_RIGHT":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\chicket_95_118x1122_1268.png',#chicket_max.png',
                                    threshold = 0.75,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [1122,95,1268,118],#crop = [700,600,1000,750],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="ZONE1":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\ZONE\\zone1.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool2,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [900,205,1235,345],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="ZONE2":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\ZONE\\zone2.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool2,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [900,205,1235,345],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="ZONE3":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\ZONE\\zone3.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool2,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [900,205,1235,345],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="ZONE4":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\ZONE\\zone4.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool2,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [900,205,1235,345],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="ZONE5":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\ZONE\\zone5.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool2,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [900,205,1235,345],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="ZONE6":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\ZONE\\zone6.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool2,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [900,205,1235,345],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="ZONE7":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\ZONE\\zone7.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool2,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [900,205,1235,345],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="ZONE8":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\ZONE\\zone8.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool2,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [900,205,1235,345],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="ZONE9":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\ZONE\\zone9.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool2,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [900,205,1235,345],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="ZONE10":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\ZONE\\zone10.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool2,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [900,205,1235,345],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="ZONE11":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\ZONE\\zone11.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool2,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [900,205,1235,345],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="ZONE12":
            return True
        elif targetimage=="DOOR_A":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\doorA.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool2,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [680,400,760,450],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="REWORD_END":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\reword_end.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool2,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [200,500,1080,720],
                                    crop_template  = []
                                    ) \
                                    or self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\reword_end2.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool2,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [200,500,1080,720],
                                    crop_template  = []
                                    ) :  
                return True
            else:
                return False
        elif targetimage=="REWORD_LOSE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\reword_lose.png',
                                    threshold = 0.85,
                                    use_gray = True,
                                    show_value = self.show_value_bool2,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [200,500,1080,720],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="MOVE_COMMENT_BATTLE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\move_comment_battle.png',
                                    threshold = 0.75,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [290,550,1000,690],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="LOSE":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\lose.png',
                                    threshold = 0.80,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [290,550,1000,690],
                                    crop_template  = []
                                    ):
                return True
            else:
                return False 
        elif targetimage=="ESCAPE_COMMENT1":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\escapecomment1.png',
                                    threshold = 0.75,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [290,550,1000,690],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="ESCAPE_COMMENT2":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\escapecomment2.png',
                                    threshold = 0.75,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [290,550,1000,690],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False 
        elif targetimage=="ESCAPE_SELECT":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\escapecommentselect.png',
                                    threshold = 0.75,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [900,400,1200,550],
                                    crop_template  = []
                                    ):  
                return True
            else:
                return False
        elif targetimage=="TARGET_LEFT":
            ret ,max_val = self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\\ZA_infi\\target_marker_left.png',
                                    threshold = 0.75,#0.72,#0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,600,550],#[100,100,1100,600],#crop = [300,100,900,600]
                                    get_max_val = True)
            #self.target_marker_Template_savelist("LEFT",max_val)
            if ret:
                return True
            else:
                return False
        elif targetimage=="TARGET_RIGHT":
            ret ,max_val = self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\\ZA_infi\\target_marker_right.png',
                                    threshold = 0.75,#0.72,#0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,600,550],#[100,100,1100,600],#crop = [300,100,900,600]
                                    get_max_val = True)
            #self.target_marker_Template_savelist("RIGHT",max_val)
            if ret:
                return True
            else:
                return False
        elif targetimage=="TARGET_LEFT_MID":
            ret ,max_val = self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\\ZA_infi\\target_marker_left.png',
                                    threshold = 0.65,#0.72,#0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,600,550],#[100,100,1100,600],#crop = [300,100,900,600]
                                    get_max_val = True)
            #self.target_marker_Template_savelist("LEFT",max_val)
            if ret:
                return True
            else:
                return False
        elif targetimage=="TARGET_RIGHT_MID":
            ret ,max_val = self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\\ZA_infi\\target_marker_right.png',
                                    threshold = 0.65,#0.72,#0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,600,550],#[100,100,1100,600],#crop = [300,100,900,600]
                                    get_max_val = True)
            #self.target_marker_Template_savelist("RIGHT",max_val)
            if ret:
                return True
            else:
                return False
        elif targetimage=="TARGET_LEFT_LOW":
            ret ,max_val = self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\\ZA_infi\\target_marker_left.png',
                                    threshold = 0.55,#0.72,#0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,600,550],#[100,100,1100,600],#crop = [300,100,900,600]
                                    get_max_val = True)
            #self.target_marker_Template_savelist("LEFT",max_val)
            if ret:
                return True
            else:
                return False
        elif targetimage=="TARGET_RIGHT_LOW":
            ret ,max_val = self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\\ZA_infi\\target_marker_right.png',
                                    threshold = 0.55,#0.72,#0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,600,550],#[100,100,1100,600],#crop = [300,100,900,600]
                                    get_max_val = True)
            #self.target_marker_Template_savelist("RIGHT",max_val)
            if ret:
                return True
            else:
                return False
        elif targetimage=="TARGET_LEFT_RIHGT_CHECK":
            ret ,max_val = self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\\ZA_infi\\target_marker_left.png',
                                    threshold = 0.75,#0.72,#0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [580,100,1280,720],#[100,100,1100,600],#crop = [300,100,900,600]
                                    get_max_val = True)
            #self.target_marker_Template_savelist("LEFT",max_val)
            if ret:
                return True
            else:
                return False
        elif targetimage=="TARGET_RIGHT_RIHGT_CHECK":
            ret ,max_val = self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\\ZA_infi\\target_marker_right.png',
                                    threshold = 0.75,#0.72,#0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [580,100,1280,720],#[100,100,1100,600],#crop = [300,100,900,600]
                                    get_max_val = True)
            #self.target_marker_Template_savelist("RIGHT",max_val)
            if ret:
                return True
            else:
                return False
        elif targetimage=="TARGET_LEFT_RIHGT_CHECK_MID":
            ret ,max_val = self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\\ZA_infi\\target_marker_left.png',
                                    threshold = 0.65,#0.72,#0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [580,100,1280,720],#[100,100,1100,600],#crop = [300,100,900,600]
                                    get_max_val = True)
            #self.target_marker_Template_savelist("LEFT",max_val)
            if ret:
                return True
            else:
                return False
        elif targetimage=="TARGET_RIGHT_RIHGT_CHECK_MID":
            ret ,max_val = self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\\ZA_infi\\target_marker_right.png',
                                    threshold = 0.65,#0.72,#0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [580,100,1280,720],#[100,100,1100,600],#crop = [300,100,900,600]
                                    get_max_val = True)
            #self.target_marker_Template_savelist("RIGHT",max_val)
            if ret:
                return True
            else:
                return False
        elif targetimage=="TARGET_LEFT_RIHGT_CHECK_LOW":
            ret ,max_val = self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\\ZA_infi\\target_marker_left.png',
                                    threshold = 0.55,#0.72,#0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [580,100,1280,720],#[100,100,1100,600],#crop = [300,100,900,600]
                                    get_max_val = True)
            #self.target_marker_Template_savelist("LEFT",max_val)
            if ret:
                return True
            else:
                return False
        elif targetimage=="TARGET_RIGHT_RIHGT_CHECK_LOW":
            ret ,max_val = self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\\ZA_infi\\target_marker_right.png',
                                    threshold = 0.55,#0.72,#0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [580,100,1280,720],#[100,100,1100,600],#crop = [300,100,900,600]
                                    get_max_val = True)
            #self.target_marker_Template_savelist("RIGHT",max_val)
            if ret:
                return True
            else:
                return False  
        elif targetimage=="ATTACK_DISPLAY":
            ret ,max_val = self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\\ZA_infi\\attack_display.png',
                                    threshold = 0.7,#0.72,#0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,600,650],#[100,100,1100,600],#crop = [300,100,900,600]
                                    get_max_val = True)
            #self.attack_display_Template_savelist("LEFT",max_val)
            if ret:
                return True
            else:
                return False
        elif targetimage=="ATTACK_DISPLAY_RIHGT_CHECKW":
            ret ,max_val = self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\\ZA_infi\\attack_display.png',
                                    threshold = 0.7,#0.72,#0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [580,100,880,720],#[100,100,1100,600],#crop = [300,100,900,600]
                                    get_max_val = True)
            #self.attack_display_Template_savelist("RIGHT",max_val)
            if ret:
                return True
            else:
                return False
        elif targetimage=="ATTACK_C+_DISPLAY":
            ret ,max_val = self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\\ZA_infi\\attack_display.png',
                                    threshold = 0.7,#0.72,#0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [0,100,600,650],#[100,100,1100,600],#crop = [300,100,900,600]
                                    get_max_val = True)
            #self.attack_display_Template_savelist("LEFT_C",max_val)
            if ret:
                return True
            else:
                return False
        elif targetimage=="ATTACK_C+_DISPLAY_RIHGT_CHECKW":
            ret ,max_val = self.isContainTemplateUltra_get_max_val(          
                                    template_path ='ZA_Story\\ZA_infi\\attack_display.png',
                                    threshold = 0.7,#0.72,#0.75,
                                    use_gray = False,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [580,100,880,720],#[100,100,1100,600],#crop = [300,100,900,600]
                                    get_max_val = True)
            #self.attack_display_Template_savelist("RIGHT_C",max_val)
            if ret:
                return True
            else:
                return False
        elif targetimage=="R_push":
            if self.isContainTemplateUltra_get_max_val(                
                                    template_path ='ZA_Story\\ZA_infi\\R_push.png',
                                    threshold = 0.75,
                                    use_gray = True,
                                    show_value = self.show_value_bool,
                                    show_position = True,
                                    show_only_true_rect  = False,
                                    ms  = 2000,
                                    crop = [1000,565,1280,720],#[1150,565,1260,620],
                                    crop_template  = []):
                return True
            else:
                return False
        return False 
        
######################################################
# テストコード
######################################################
        
    def Test(self):
        self.show_value_bool = True
        while True:
            self.checkIfAlive()
                
            if self.image_check("2_SELECT"):
                print("2_SELECT")
            self.wait(2.0)
        return True
            
    def Testimagecheck(self,num):
        if num == 1:
            print("test")
            
######################################################
# こっからがコマンド
######################################################               
class ZA_story(ZA_story_Base):
    version_major = 0
    version_minor = 0
    version_patch = 0
    
    ZA_infimode=0
    
    if ZA_infimode==1:
        ZA_infi_custom_name = "_ZA_infi_custom_name"
    else:
        ZA_infi_custom_name = ""
    
    NAME = f'ZA_story_v{version_major}.{version_minor}.{version_patch}{ZA_infi_custom_name}'
    def __init__(self, cam):
        super().__init__(cam)
    def do(self):
        # スクリプト継承
        if self.testcode==1:
            self.Test()
        elif ZA_story.ZA_infimode==1:
            self.ZA_battle_infi_main()
        else:
            self.ZA_story_main()