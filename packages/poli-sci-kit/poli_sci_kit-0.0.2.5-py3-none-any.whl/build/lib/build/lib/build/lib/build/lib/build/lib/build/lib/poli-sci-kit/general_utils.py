# =============================================================================
# Utility functions for data manipulation and processing
#
# Contents
# --------
#   0. No Class
#       separate_disputed
#       combine_dependency
#       graph_inputs
#       freedom_house_category_ratios
# =============================================================================

import numpy as np
import pandas as pd
import seaborn as sns

fig_fontsize = 20

def separate_disputed(df, col, region, disputed=None):
    """
    Subtracts the populations of disputed regions from the occupying region

    Parameters
    ----------            
        df : pd.DataFrame
            Regional data including population size
            
        col : str
            The column in df in which regions are defined
        
        region : str
            The region in which disputed territories are to be removed from

        disputed : str or list (default=None)
            The disputed region to be separated
            Data formated such that disputed regions have their occupying region in parentheses 'disputed (region)'
        
    Returns
    -------
        df with the population of the disputed region subtracted from the occupying region, as well as formatting
    """
    assert region in [name for name in df[col]], '{} is not in the data.'.format(region)
    # Assert that the region is included in those that have territories
    assert '({})'.format(region) in [name.split()[1] if len(name.split()) > 1 else '({})'.format(region) for name in df[col]], 'There are no disputed regions of {} in the data.'.format(region)

    if disputed == None:
        disputed_indexes = [i for i in df.index if '({})'.format(region) in df.loc[i, col]]

    elif type(disputed) == str:
        assert '{} ({})'.format(disputed, region) in [name for name in df[col]], "{} is not in the data, or doesn't match {}.".format(disputed, region)
        
        disputed_indexes = [df[df[col] == '{} ({})'.format(disputed, region)].index[0]]
    
    elif type(disputed) == list:
        disputed_indexes = []
        for d in disputed:
            assert '{} ({})'.format(d, region) in [name for name in df[col]], "{} is not in the data, or doesn't match {}.".format(d, region)
            
            disputed_indexes.append(df[df[col] == '{} ({})'.format(d, region)].index[0])

    else:
        print("Invalid type for 'disputed' argument")
        
        return
    
    region_index = df[df[col] == region].index[0]
    
    for i in disputed_indexes:
        df.loc[region_index, 'population'] -= df.loc[i, 'population']
        df.loc[i, col] = df.loc[i, col].split('(')[0][:-1] # rename for output
        print('The population of {} was deducted from {}, which is now {}.'.format(df.loc[i, col], 
                                                                                   region,
                                                                                   str(df.loc[region_index, 'population'])))


def combine_dependency(df, col, region, dependent=None):
    """
    Combines the populations of undisputed territories to the occupying region

    Parameters
    ----------            
        df : pd.DataFrame
            Regional data including population size
            
        col : str
            The column in df in which regions are defined

        region : str
            The region in which dependent territories are to be removed from

        dependent : str or list
            The dependent region to be combined
            Data formated such that dependent regions have their occupying region in parentheses 'dependent (region)'
        
    Returns
    -------
        df with the population of the dependent region added to the occupying region, as well as dropping dependent row
    """
    assert region in [name for name in df[col]], '{} is not in the data.'.format(region)
    # Assert that the region is included in those that have territories
    assert '({})'.format(region) in [name.split()[1] if len(name.split()) > 1 else '({})'.format(region) for name in df[col]], 'There are no dependent regions of {} in the data.'.format(region)
    
    if dependent == None:
        dependent_indexes = [i for i in df.index if '({})'.format(region) in df.loc[i, col]]

    elif type(dependent) == str:
        assert '{} ({})'.format(dependent, region) in [name for name in df[col]], "{} is not in the data, or doesn't match {}.".format(dependent, region)
        
        dependent_indexes = [df[df[col] == '{} ({})'.format(dependent, region)].index[0]]
    
    elif type(dependent) == list:
        dependent_indexes = []
        for d in dependent:
            assert '{} ({})'.format(d, region) in [name for name in df[col]], "{} is not in the data, or doesn't match {}.".format(dependent, region)
            
            dependent_indexes.append(df[df[col] == '{} ({})'.format(d, region)].index[0])

    else:
        print("Invalid type for 'dependent' argument")
        
        return
    
    region_index = df[df[col] == region].index[0]
    
    for i in dependent_indexes:
        df.loc[region_index, 'population'] += df.loc[i, 'population']
        df.loc[i, col] = df.loc[i, col].split('(')[0][:-1] # rename for output
        print('The population of {} was added to {}, which now has a population of {}.'.format(df.loc[i, col], 
                                                                                               region,
                                                                                               str(df.loc[region_index, 'population'])))
        df.drop(i, inplace=True)


def graph_inputs(df, col, subset=None, subset_col=None, 
                 input_type='Population', fontsize=fig_fontsize, axis=None):
    """
    Plots either:
        - A plot of appointment inputs for all regions or parties with subsets being hues (larger displays suggested)
        - A plot for a distinct subset

    Parameters
    ----------            
        df : pd.DataFrame
            Regional data including population size
            
        col : str
            The column in df in which regions are defined

        subset : str : optional (default=None)
            The subset of the regions for which the graph should be made

        input_type : str (default=Population, option=Votes)
            Whether the graph is of population inputs or votes

        subset_col : ste : optional (default=None)
            The column in df in which subsets are defined

        fontsize : int or float : optional (default=20)
            The font size of the plots, with all labels scaled accordingly
            
        axis : str : optional (default=None)
            Adds an axis to the plot so they can be combined
        
    Returns
    -------
        A population or votes bar plot
    """
    if subset is not None:
        assert subset_col is not None, "Please provide the column name for subsets with the 'subset_col' argument."
        assert subset in [s for s in df[subset_col]], '{} is not a subset in the data.'.format(subset)
        
        df = df[df[subset_col] == subset]
        ax = sns.barplot(data=df, x=col, y=input_type.lower(), ax=axis)
        ax.axes.set_title('{} per {} ({})'.format(input_type.capitalize(), col.capitalize(), subset), fontsize=fig_fontsize*1.5)
        
    else:
        ax = sns.barplot(data=df, x=col, y=input_type.lower(), hue=subset_col, ax=axis)
        ax.axes.set_title('{} per {}'.format(input_type.capitalize(), col.capitalize()), fontsize=fig_fontsize*1.5)
        
    ax.set_xlabel(col.capitalize(), fontsize=fig_fontsize)
    ax.set_ylabel('{}'.format(input_type.capitalize()), fontsize=fig_fontsize)
    ax.set_xticklabels(ax.get_xticklabels(),rotation=60)


def freedom_house_category_ratios(df, subset=None, subset_col=None):
    """
    Prints either:
        - The percents of Freedom House categories over the data
        - The percents for a distinct subset

        - Populations included for the above for comparison

    Parameters
    ----------            
        df : pd.DataFrame
            Regional data including population size

        subset : str : optional (default=None)
            The subset of the countries on which the graph should be made

        subset_col : ste : optional (default=None)
            The column in df in which subsets are defined
        
    Returns
    -------
        Pecents of Freedom House categories and populations
    """
    if subset is not None:
        assert subset_col is not None, "Please provide the column name for subsets with the 'subset_col' argument."
        assert subset in [s for s in df[subset_col]], '{} is not in the data.'.format(subset)
    
        df = df.loc[df[subset_col] == subset]
    
    # The populations for comparison, and adding commas so it's eaiser to read (reverse and then return order)
    total_pop = df['population'].sum()
    total_pop_str = str(total_pop)
    total_pop_str = [i for i in total_pop_str]
    total_pop_str[::-1]
    
    total_pop_with_commas = [total_pop_str[i]+',' if i % 3 == 0 and i != 0 else total_pop_str[i] for i in range(len(total_pop_str))]
    total_pop_with_commas[::-1]
    
    total_pop_display = ''
    for i in total_pop_with_commas:
        total_pop_display += i

    if subset == None:
        subset = 'World'

    print('{}: {} countries; {} people'.format(subset, len(df), total_pop_display))
    print(df['freedom_house_category'].value_counts()/len(df))