import pandas as pd
from typing import List
from turpy.logger import log


def __subset_generator(
    df: pd.DataFrame, 
    is_row_one: pd.Series = None, 
    video_section_id: str = 'video_section_id'):

    """Creates a subset of the raw dropvideo transect to be summarised.

    :param df:
    :param is_row_one: hold a boolean series of indexes where `True`
        is the starting point of the transect to be summarized, ie. frames(pictures)
        It is expected to have 10 frames + 1 Hela: value, e.g. 11 values.
    :param video_section_id: column name holding the `video_section_id` also known as
        the frame id where the video dots are accounted. 
        Raw dropvideo has 10 frames as rows + 1 presence row summary.
        Expected series as [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Hela'] * number of stations
    
    :return:
        subset and index of start of the subset
    """
    if is_row_one is None:
        is_row_one = df[video_section_id].astype(str) == '1'

    for i in is_row_one.index:
        is_true = is_row_one[i]
        if is_true:
            subset = df.loc[i:i+10, :]
            yield subset, i


def dropvideo_section_to_aggregate(df: pd.DataFrame, colnames:list, video_section_id: str ='video_section_id'):
    """Summarizes biota occurrences in the raw dropvideo dataframe

    :param df: Pandas Dataframe with the raw dropvideo data
    :param log_kvargs:
    :return:
    """
    
    # NOTE: `pict_numb` cannot be used to check if is a raw dropvideo file, as this column may exist for
    # summarized dropvideo datasets, but with a single value like 1, as in
    # Epibenthos_dropvideo_X_C_lst_AQBI_2016_cover.tsv

    if video_section_id in df:
        # NOTE: `pict_numb`

        is_row_one = df[video_section_id].astype(str) == '1'
        # checking that we would have 11 rows to summarize, else report as error and do nothing

        if len(is_row_one) % 11 == 0:

            log.info(
                '`video_section_id` detected. Preparing raw dropvideo file')
            log.info('Summarizing dropvideo ...')
            log.info(f'`{len(df)}` records to summarize')

            # Initialization #############################################
            
            df_holder = df[is_row_one].copy()
            log.info('Summarizing Dropvideo `colnames`')

            for subset, i in __subset_generator(df=df, is_row_one=is_row_one):

                for col in colnames:
                    # NEW API [2019-01-23]
                    check_presence = subset[col].iloc[10]
                    is_presence = 1 if check_presence != "" and float(
                        check_presence) > 0 else 0
                    #
                    try:
                        percent_cover = sum([int(float(x)) for x in list(
                            subset[col].iloc[0:10]) if x not in ['', ' ', None]])
                    except Exception as msg:
                        log.error('initialization_raw_dropvideo_subset_colnames: index: `{}`,  '
                                     'subset : `{}`, error_message: `{}`'.format(i, subset[col], msg))

                        
                        return {'is_troublesome': True}
                    else:
                        #TESTME: THE CODE BELOW REQUIRES BETTER TESTING AS IT COULD BE TROUBLED # [2019-01-23]
                        if percent_cover == 0:
                            if is_presence:
                                #print(
                                #    'i: `{}` col: `{}`, df_holder[i, col]: `{}` will be set to True'.format(i, col, df_holder.loc[i, col]))
                                df_holder.loc[i, col] = 1
                                # print('we have presence and not percent_cover') ## DEBUG THIS MAY NOT BE TRUE IF THE BIOTA WAS ACTUALLY ZERO
                            else:
                                df_holder.loc[i, col] = ''

                        else:
                            df_holder.loc[i, col] = percent_cover
            
            #
            log.info('RAW Dropvideo has being summarized.')
            df_holder.reset_index(drop=True, inplace=True)
            df = df_holder

            return df

        else:
            log.warning('Dropvideo cannot be summarized. Is it really a RAW dropvideo file? '
                           'make sure you have exactly 11 rows to summarize for each station. '
                           'Please DEBUG input file.')
            
            return {'is_troublesome': True}
    else:
        log.info(
            'No raw dropvideo detected. Continue safely. Doing nothing!')
        return df
