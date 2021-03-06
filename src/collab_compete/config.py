

import os
import torch
from src import utils
from src.buffer import MemoryER
from src.exploration import OUNoise
# from src.collab_compete.model import Actor, Critic
from src.logger import Logger


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


# class Config:
#     import os
#     # ENVIRONMEMT PARAMETER
#
#     STATE_SIZE = 24
#     ACTION_SIZE = 2
#     NUM_AGENTS = 2
#     NUM_EPISODES = 1000
#     NUM_TIMESTEPS = 1000
#     #
#     # # MODEL PARAMETERS
#     # SEED = 0
#     BUFFER_SIZE = int(1e05)
#     BATCH_SIZE = 512
#     DATA_TO_BUFFER_BEFORE_LEARNING = BATCH_SIZE
#
#     # Exploration parameter
#     NOISE_AMPLITUDE_FN = lambda: utils.Decay(
#             alpha=2, decay_rate=0.999, min_value=0.001,
#             start_decay_after_step=Config.DATA_TO_BUFFER_BEFORE_LEARNING).multiplicative_decay
#     EXPLORATION_POLICY_FN = lambda: OUNoise(size=Config.ACTION_SIZE, seed=2)
#
#     # LEARNING PARAMETERS
#     ACTOR_LEARNING_RATE = 0.0001
#     CRITIC_LEARNING_RATE = 0.0001
#     GAMMA = 0.998  # Discounts
#     LEARNING_FREQUENCY = 16
#
#     # WEIGHTS UPDATE PARAMETERS
#     SOFT_UPDATE = False
#     TAU = 0.01  # Soft update parameter for target_network
#     SOFT_UPDATE_FREQUENCY = 32
#     DECAY_TAU = False
#     TAU_DECAY_RATE = 0.003
#     TAU_MIN = 0.05
#
#     HARD_UPDATE = True
#     HARD_UPDATE_FREQUENCY = 1000
#
#
#     if (SOFT_UPDATE and HARD_UPDATE) or (not SOFT_UPDATE and not HARD_UPDATE):
#         raise ValueError('Only one of Hard Update and Soft Update is to be chosen ..')
#
#     if SOFT_UPDATE_FREQUENCY < LEARNING_FREQUENCY:
#         raise ValueError('Soft update frequency can not be smaller than the learning frequency')
#
#     ################### Lambda Functions:
#     # Agent-1 and Agent-2
#     ACTOR_NETWORK_FN = [
#         lambda: Actor(
#             Config.STATE_SIZE, Config.ACTION_SIZE, layer_in_out=[256, 256, 2], seed=345
#         ).to(device),
#
#         lambda: Actor(
#                 Config.STATE_SIZE, Config.ACTION_SIZE, layer_in_out=[256, 256, 2], seed=842
#         ).to(device)
#     ]
#
#     CRITIC_NETWORK_FN = [
#         lambda: Critic(
#             Config.STATE_SIZE, Config.ACTION_SIZE, seed=982, layer_in_out=[256, 256, 2]
#         ).to(device),
#
#         lambda: Critic(
#                 Config.STATE_SIZE, Config.ACTION_SIZE, seed=665, layer_in_out=[256, 256, 2]
#         ).to(device)
#     ]
#
#     ACTOR_OPTIMIZER_FN = lambda params: torch.optim.Adam(params, lr=Config.ACTOR_LEARNING_RATE)
#     CRITIC_OPTIMIZER_FN = lambda params: torch.optim.Adam(params, lr=Config.ACTOR_LEARNING_RATE)
#
#     # Agent Memory-Buffer and Scores
#     MEMORY_FN = lambda: MemoryER(Config.BUFFER_SIZE, Config.BATCH_SIZE, seed=2, action_dtype='float')
#     SCORES_FN = lambda param: utils.Scores(episode_score_window=100, agent_id=param)
#
#     # LOG PATHS
#     MODEL_NAME = 'model_1'
#     pth = os.path.abspath(os.path.join(os.getcwd(), '../..'))
#     model_dir = pth + '/models'
#     base_dir = os.path.join(model_dir, 'collab_compete', '%s' % (MODEL_NAME))
#
#     if not os.path.exists(base_dir):
#         print('creating .... ', base_dir)
#         os.makedirs(base_dir)
#
#     CHECKPOINT_DIR = base_dir
#     STATS_JSON_PATH = os.path.join(base_dir, 'stats.json')
#     SUMMARY_LOGGER_PATH = os.path.join(base_dir, 'summary')
#
#     if not os.path.exists(SUMMARY_LOGGER_PATH):
#         print('creating .... ', SUMMARY_LOGGER_PATH)
#         os.makedirs(SUMMARY_LOGGER_PATH)
#
#     SUMMARY_LOGGER = Logger(SUMMARY_LOGGER_PATH)




class TrainConfig:
    # Environment Parameters
    SEED = 0
    STATE_SIZE = 24
    ACTION_SIZE = 2
    NUM_AGENTS = 2
    BUFFER_SIZE = 10000
    BATCH_SIZE = 256
    
    # Agent Params
    TAU = 1e-3
    WEIGHT_DECAY = 0.0
    IS_HARD_UPDATE = False
    IS_SOFT_UPDATE = True
    SOFT_UPDATE_FREQUENCY = 2
    HARD_UPDATE_FREQUENCY = 2000
    
    
    # Model parameters
    ACTOR_LEARNING_RATE = 1e-4
    CRITIC_LEARNING_RATE = 1e-3
    DATA_TO_BUFFER_BEFORE_LEARNING = 256
    GAMMA = 0.99
    LEARNING_FREQUENCY = 2

    # Exploration parameter
    NOISE_FN = lambda: OUNoise(size=2, seed=0)  # (ACTION_SIZE, SEED_VAL)
    NOISE_AMPLITUDE_DECAY_FN = lambda: utils.Decay(
            decay_type='multiplicative',
            alpha=1, decay_rate=0.995, min_value=0.25,
            start_decay_after_step=15000,
            decay_after_every_step=100,
            decay_to_zero_after_step=30000
    )
    

    # LOG PATHS
    MODEL_NAME = 'model_4'
    pth = os.path.abspath(os.path.join(os.getcwd(), '../..'))
    model_dir = pth + '/models'
    base_dir = os.path.join(model_dir, 'collab_compete', '%s' % (MODEL_NAME))

    if not os.path.exists(base_dir):
        print('creating .... ', base_dir)
        os.makedirs(base_dir)

    CHECKPOINT_DIR = base_dir
    STATS_JSON_PATH = os.path.join(base_dir, 'stats.json')
    SUMMARY_LOGGER_PATH = os.path.join(base_dir, 'summary')

    if not os.path.exists(SUMMARY_LOGGER_PATH):
        print('creating .... ', SUMMARY_LOGGER_PATH)
        os.makedirs(SUMMARY_LOGGER_PATH)

    SUMMARY_LOGGER = Logger(SUMMARY_LOGGER_PATH)
    
    
    
    # Exception checking
    if (IS_SOFT_UPDATE and IS_HARD_UPDATE) or (not IS_SOFT_UPDATE and not IS_HARD_UPDATE):
        raise ValueError('Only one of Hard Update and Soft Update is to be chosen ..')

    if SOFT_UPDATE_FREQUENCY < LEARNING_FREQUENCY:
        raise ValueError('Soft update frequency can not be smaller than the learning frequency')


class TestConfig:
    # Environment Parameters
    SEED = 0
    STATE_SIZE = 24
    ACTION_SIZE = 2
    NUM_AGENTS = 2
    
    
    # Exploration parameter
    NOISE_FN = None
    NOISE_AMPLITUDE_DECAY_FN = None
    
    # LOG PATHS
    MODEL_NAME = 'model_3'
    CHECKPOINT_NUMBER = '1029'
    pth = os.path.abspath(os.path.join(os.getcwd(), '../..'))
    model_dir = pth + '/models'
    base_dir = os.path.join(model_dir, 'collab_compete', '%s' % (MODEL_NAME))
    
    if not os.path.exists(base_dir):
        print('creating .... ', base_dir)
        os.makedirs(base_dir)
    
    CHECKPOINT_DIR = base_dir
    
