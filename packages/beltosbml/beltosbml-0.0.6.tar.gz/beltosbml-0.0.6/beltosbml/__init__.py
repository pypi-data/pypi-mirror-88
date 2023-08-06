#!/usr/bin/env python
# coding: utf-8

# # Pipeline for Extending SBML Model with BEL Edges

# ## Dependencies

# ### Installations

# In[3]:


# Uncomment the following lines below as needed.
# It is recommended to first run the entire cell
# then run the second section below into the term

# !pip install python_libsbml
# !pip install numpy
# !pip install pandas
# !pip install requests
# !pip install matplotlib
# !pip install tabulate
# !pip install pypesto
# !pip install -e git+https://github.com/icb-dcm/amici.git@develop#egg=amici\&subdirectory=python/sdist #on Fedora machines make sure you have `run sudo dnf install blas-devel`
# !pip install petab
# !pip install ebel-rest

# The following installations must be run in the terminal:
#pip install git+https://gitlab.scai.fraunhofer.de/biodev/bel/ebel_rest.git
#conda install -c conda-forge openblas


# ### Imports

# In[4]:


# Import block
#import amici
#import amici.plotting

#from petab.visualize import plot_data_and_simulation
#import pypesto
#import pypesto.visualize as visualize
#import pypesto.optimize as optimize

import sys
import os
import site

import numpy as np
import pandas as pd
from tabulate import tabulate

import urllib.parse
import urllib.request
import requests
import json

from ebel_rest import connect, query, statistics
import getpass

from typing import List, Tuple
import re

import libsbml
import importlib

import pprint

import matplotlib as mpl
import matplotlib.pyplot as plt

# Import end

#env = %env
#access_notebook_information(dict(globals())['_ih'][1], env)


# ## Functions

# ### AMICI - Simulation

# In[5]:


def simulate_trajectories(sbml_file, observables = "", verbose=False):
    print("Currently simulating for: " + str(sbml_file))
    model_name = sbml_file.split("/")[-1].split(".")[0]+'_simulation_model'
    # Directory to which the generated model code is written
    model_output_dir = model_name

    if os.path.isfile(model_output_dir):
        os.remove(model_output_dir)

    sbml_reader= libsbml.SBMLReader()
    sbml_doc = sbml_reader.readSBML(sbml_file)
    sbml_model = sbml_doc.getModel()

    # Create an SbmlImporter instance for our SBML model
    sbml_importer = amici.SbmlImporter(sbml_file)

    # Define observables
    observables = {
        # 'observable_Bp': {'name': '', 'formula': 'Bp'},
        'observable_Ab': {'name': '', 'formula': 'Ap'},
        #'observable_TauH3Rwithsigma': {'name': '', 'formula': 'TauH3R'}
    }
    #$\sigma$ parameters
    #sigmas = {'observable_TauH3Rwithsigma': 'observable_TauH3Rwithsigma_sigma'}


    #Generating the module
    sbml_importer.sbml2amici(model_name,
                             model_output_dir,
                             #verbose=logging.INFO,
                             observables=observables,
                             #This line can eventually have drug administration, e.g..
                             #constant_parameters=constantParameters,
                             #sigmas=sigmas
                            )

    # Importing the module and loading the model
    sys.path.insert(0, os.path.abspath(model_output_dir))
    model_module = importlib.import_module(model_name)


    model = model_module.getModel()

    print("Model name:", model.getName())
    if verbose:
        print("Model parameters:", model.getParameterIds())
        print("Model outputs:   ", model.getObservableIds())
        print("Model states:    ", model.getStateIds())

    #Running simulations and analyzing results
    # Create Model instance
    model = model_module.getModel()

    # set timepoints for which we want to simulate the model
    model.setTimepoints(np.linspace(0, 60, 60))

    # Create solver instance
    solver = model.getSolver()

    # Run simulation using default model parameters and solver options
    rdata = amici.runAmiciSimulation(model, solver)

    # Create ExpData instance from simulation results
    edata = amici.ExpData(rdata, 1.0, 0.0)

    # Re-run simulation, this time passing "experimental data"
    rdata = amici.runAmiciSimulation(model, solver, edata)

    if verbose:
        print('Simulation was run using model default parameters as specified in the SBML model:')
        print(model.getParameters())
        print('Log-likelihood %f' % rdata['llh'])

        #np.set_printoptions(threshold=8, edgeitems=2)
        for key, value in rdata.items():
            print('%12s: ' % key, value)



    # look at the States in rdata as DataFrame
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    amici.getSimulationStatesAsDataFrame(model, [edata], [rdata])

    return amici.getSimulationStatesAsDataFrame(model, [edata], [rdata])


# ### libsbml

# In[6]:


def create_unit_definitions(model, unit_id):
    unitDefinition = model.createUnitDefinition()
    unitDefinition.setId(unit_id)
    unitDefinition.setName(unit_id)
    unit = unitDefinition.createUnit()
    unit.setKind(UNIT_KIND_DIMENSIONLESS)

def create_species(model: libsbml.Model, s_id: str, compartment: str,
                   constant: bool = False, initial_amount: float = 0.0,
                   substance_units: str = 'nanoMole', meta_id: str = '',
                   boundary_condition: bool = False,
                   has_only_substance_units: bool = False) -> None:
    """
    Creates new species for libsbml.Model
    :param model: libsbml.Model for which species will be created
    :param s_id: species id for the new species
    :param compartment: compartment to which new species will be assigned
    :param constant: True if the new species should be constant
    :param initial_amount: start value for species
    :param substance_units: substance unit for species
    :param boundary_condition: True if there is a boundary condition
    :param has_only_substance_units: True if species has only substance units
    """
    s = model.createSpecies()
    s.setId(s_id)
    s.setMetaId(str(meta_id))
    #s.addCVTerm(str(s_id))
    s.setName(s_id)
    s.setCompartment(compartment)
    s.setConstant(constant)
    s.setInitialAmount(initial_amount)
    s.setSubstanceUnits(substance_units)
    s.setBoundaryCondition(boundary_condition)

    return s

def create_parameter(model: libsbml.Model, p_id: str, constant: bool,
                     value: float, units: str) -> None:
    """
    Creates new parameter for libsbml.Model
    :param model: libsbml.Model to which new parameter will be added
    :param p_id: Id for the new parameter
    :param constant: True if the new parameter should be constant
    :param value: Initial value of the parameter
    :param units: Units for the parameter
    """
    k = model.createParameter()
    k.setId(p_id)
    k.setName(p_id)
    k.setConstant(constant)
    k.setValue(value)
    k.setUnits(units)

    return k

def create_reaction(model: libsbml.Model, m_id: str,
                    reactants: List[Tuple[int, str]],
                    products: List[Tuple[int, str]],
                    formula: str, modifiers: List[str] = None,
                    reversible: bool = False, fast: bool = False) -> None:
    """
    Creates new reaction for libsbml.Model
    :param model: libsbml.Model to which new reaction will be added
    :param m_id: Id for the new reaction
    :param reactants: List or reactants of the reaction
    :param products: List of products of the reaction
    :param formula: Formula for the rate of the reaction
    :param modifiers: List of modifiers of the reaction
    :param reversible: True if the reaction should be reversible
    :param fast: True if the reaction should be fast
    """
    if modifiers is None:
        modifiers = []
    r = model.createReaction()
    r.setId(m_id)
    r.setReversible(reversible)
    r.setFast(fast)

    for (coeff, name) in reactants:
        species_ref = r.createReactant()
        species_ref.setSpecies(name)
        species_ref.setConstant(True)  # TODO ?f
        species_ref.setStoichiometry(coeff)
    for (coeff, name) in products:
        species_ref = r.createProduct()
        try:
            species_ref.setSpecies(str(name))
        except:
            print('Cant convert this: '+name+' to valid SBML name')
        species_ref.setConstant(True)  # TODO ?
        species_ref.setStoichiometry(coeff)
    for name in modifiers:
        species_ref = r.createModifier()
        species_ref.setSpecies(name)
        # species_ref.setConstant(True)  # TODO ?

    math_ast = libsbml.parseL3Formula(formula)
    kinetic_law = r.createKineticLaw()
    kinetic_law.setMath(math_ast)

    return r

def create_assigment_rule(sbml_model: libsbml.Model,
                          assignee_id: str,
                          formula: str,
                          rule_id: str = None,
                          rule_name: str = None) -> libsbml.AssignmentRule:
    """Create SBML AssignmentRule
    Arguments:
        sbml_model: Model to add output to
        assignee_id: Target of assignment
        formula: Formula string for model output
        rule_id: SBML id for created rule
        rule_name: SBML name for created rule
    Returns:
        The created ``AssignmentRule``
    """
    if rule_id is None:
        rule_id = assignee_id

    if rule_name is None:
        rule_name = rule_id

    rule = sbml_model.createAssignmentRule()
    rule.setId(rule_id)
    rule.setName(rule_name)
    rule.setVariable(assignee_id)
    rule.setFormula(formula)

    return rule

def create_initial_assigment(sbml_model: libsbml.Model,
                             assignee_id: str,
                             formula: str,
                             rule_id: str = None,
                             rule_name: str = None) -> libsbml.InitialAssignment:
    """Create SBML InitialAssignment
    Arguments:
        sbml_model: Model to add output to
        assignee_id: Target of assignment
        formula: Formula string for model output
        rule_id: SBML id for created rule
        rule_name: SBML name for created rule
    Returns:
        The created ``InitialAssignment``
    """
    if rule_id is None:
        rule_id = assignee_id

    if rule_name is None:
        rule_name = rule_id

    rule = sbml_model.createInitialAssignment()
    rule.setId(rule_id)
    rule.setName(rule_name)
    rule.setSymbol(assignee_id)
    math_ast = libsbml.parseL3Formula(formula)
    rule.setMath(math_ast)

    return rule


# ### ebel_rest

# In[7]:


def retrieve_bel_edges_rest(auth:dict = dict(),
                        df:pd.DataFrame = pd.DataFrame(),
                        out_node:str = None,
                        in_node:str = None):
    '''
    Retrieves bel edges via ebel REST API and returns a dataframe
    todo: write final documentation
    '''
    # Database settings

    print_url = True

    # Connect to database
    connect(auth['user'], auth['password'], auth['server'], auth['db_name'], print_url)

    if out_node == None:
        query_df = query.sql("SELECT out.bel, @class, in.bel, annotation, pmid           FROM bel_relation WHERE           out.name.toLowerCase() LIKE '%"+in_node.lower()+"%'").table
        assert type(query_df) == pd.DataFrame, "Dataframe not returned - query probably returned no results."
        df = df.append(query_df)
        return df
    if in_node == None:
        query_df = query.sql("SELECT out.bel, @class, in.bel, annotation, pmid           FROM bel_relation WHERE           in.name.toLowerCase() LIKE '%"+out_node.lower()+"%'").table
        assert type(query_df) == pd.DataFrame, "Dataframe not returned - query probably returned no results."
        df = df.append(query_df)
        return df
    query_df = query.sql("SELECT out.bel, @class, in.bel, annotation, pmid           FROM bel_relation WHERE           out.name.toLowerCase() LIKE '%"+out_node.lower()+"%' AND           in.name.toLowerCase() LIKE '%"+in_node.lower()+"%'").table
    assert type(query_df) == pd.DataFrame, "Dataframe not returned - query probably returned no results."
    df = df.append(query_df)
    return df


# ### BEL & SBML Syntax Translations

# In[8]:


def reformat_name_for_SBML_id(name):

    return name.replace("*","_")

def put_modifiers_in_SBML_id(mods, split):
    return '_'+split.replace('(','').replace(')','').replace(',','')

def reformat_BEL_for_SBML_id(name):
    """
    Reformates BEL syntax to acceptable SBML format

    Arguments:
        name: name from BEL
    Returns:
        id: id name with acceptable characters, Database + ID:
        e.g. HGNC_HDAC6
    """

    if 'complex' in name:
        #print('\nBEL name:'+''+name)
        splits = name.split('\"')
        #print('splits based on \" characters')
        #print(str(splits))
        mods = '' #modifications
        for i in range(1,len(splits),2):
            #print(splits[i])
            if 'pmod' in splits[i]:
                mods += put_modifiers_in_SBML_id(mods,split)
        #print("splits[0]:" + splits[0])
        SBML_id = splits[0].split(':')[0].split("(")[1] +'_'+ splits[1].replace(" ","_") + mods
        #print('new id:'+''+SBML_id)
        #todo: remove code library


    splits = name.split('\"')
    mods = '' #modifications e.g. pmod(Ac)
    for split in splits:
        if 'pmod' in split:
            mods += put_modifiers_in_SBML_id(mods,split)
    SBML_id = 'BEL_import_'+splits[0].split(':')[0].split("(")[1] +'_'+ splits[1].replace(" ","_") + mods



    return str(SBML_id)

def add_BEL_reaction_to_SBML_model(bel_row, model):
    """
    Adds BEL triplet to SBML format as a reaction

    Arguments:

    Returns:

    """

    out_node = reformat_BEL_for_SBML_id(bel_row.subject_bel)
    in_node = reformat_BEL_for_SBML_id(bel_row.object_bel)
    reaction_id = out_node+'_'+bel_row.relation+'_'+in_node

    r_id = reaction_id

    if 'increases' in bel_row.relation:
        reactants=[(1,out_node)]
        products=[(1,in_node),(1,out_node)]

    if 'decreases' in bel_row.relation:
        reactants=[(1,out_node),(1,in_node)]
        products=[(1,out_node)]

    #if the reaction doesn't already exist, create it.
    if not bool(model.reactions.getElementBySId(reaction_id)):

        #Create parameter for it
        p_id = 'parameter_'+reaction_id
        create_parameter(model, p_id = p_id, constant = True,
                 value = 8.375, units='dimensionless')

        create_reaction(model, m_id= reaction_id,
                            reactants=reactants,
                            products=products,
                            formula= p_id+'*'+out_node,
                            modifiers= None,
                                reversible=False, fast=False)
    print("The following reaction was created: "+reaction_id)
    return model

def add_bel_df_to_SBML_doc(bel_df, sbml_cv_df, sbml_model, initial_amount_subject = 1,initial_amount_object = 1, reaction_rate = 1):

    # create species from out and in (subject and object) nodes of BEL statement and respective reactions
    for index, row in bel_df.iterrows():
        # if species exist in the model, refer to it
        if (any(sbml_cv_df.cv_ids.isin([row.subject_uniprots]))):
            print("Match found for subject for existing species within the model.")
            subject_species = sbml_model.getElementBySId(sbml_cv_df.iloc[sbml_cv_df.cv_ids[sbml_cv_df.cv_ids.isin([row.subject_uniprots])].index].element_reference.values[0])
        else:
            subject_species = create_species(sbml_model,
                                         s_id=reformat_BEL_for_SBML_id(row['out']),
                                         compartment = 'Brain',
                                         constant = False, initial_amount = initial_amount_subject,
                                         substance_units = 'dimensionless',
                                         boundary_condition = False,
                                         has_only_substance_units = False)
        if (any(sbml_cv_df.cv_ids.isin([row.object_uniprots]))):
            print("Match found object for existing species within the model.")
            object_species = sbml_model.getElementBySId(sbml_cv_df.iloc[sbml_cv_df.cv_ids[sbml_cv_df.cv_ids.isin([row.object_uniprots])].index].element_reference.values[0])
        else:
            object_species = create_species(sbml_model,
                                     s_id=reformat_BEL_for_SBML_id(row['in']),
                                     compartment = 'Brain',
                                     constant = False, initial_amount = initial_amount_object,
                                     substance_units = 'dimensionless',
                                     boundary_condition = False,
                                     has_only_substance_units = False)
        reactants, products = bel_relation_type_to_reaction_kinetics(subject_species.id, object_species.id, row['class'])
        reaction_id = create_reaction_id(reactants,products)
        new_reaction = create_reaction(sbml_model,
                    m_id= reaction_id,
                    reactants=reactants,
                    products=products,
                    formula= str(reaction_rate)+'*'+str(reactants[0][1])+str(reactants[0][1]),
                    modifiers= None,
                    reversible=False, fast=False)
        print("The following reaction was created within the simulation: "+reaction_id)
        print("Here is an updated list of the species:")
        print(get_model_species_cv_df(sbml_model)['element_reference'])
        print("Here is an updated list of the reactions:")
        print(sbml_model.getListOfReactions()[:])
    return sbml_model

def add_assay_df_to_SBML_doc(assay_df, SBML_document):
    model = SBML_document.getModel()

    for c_id_entry in assay_df['Compound Id'].unique():

        cas_num = 'CAS_num_'+ str(assay_df.loc[assay_df['Compound Id'] == c_id_entry]['CAS#'].values[0]).replace("-","_").replace(".","_").replace(" ","_")
        initial_amount = assay_df.loc[assay_df['Compound Id'] == c_id_entry]['Assay Concentration (æM)'].values[0].item()
        value = assay_df.loc[assay_df['Compound Id'] == c_id_entry]['% Inhibition (HDAC6)'].values[0].item()


        create_species(model, s_id = cas_num,
                           compartment = 'Brain',
                           constant = False, initial_amount = initial_amount,
                           substance_units = 'dimensionless',
                           boundary_condition = False,
                           has_only_substance_units = False)

    return SBML_document

def generate_new_SBML_doc_for_intervention(assay_df, SBML_document):
    model = SBML_document.getModel()

    for c_id_entry in assay_df['Compound Id'].unique():
        cas_num = 'CAS_num_'+ str(assay_df.loc[assay_df['Compound Id'] == c_id_entry]['CAS#'].values[0]).replace("-","_").replace(".","_").replace(" ","_")
        initial_amount = assay_df.loc[assay_df['Compound Id'] == c_id_entry]['Assay Concentration (æM)'].values[0].item()
        value = assay_df.loc[assay_df['Compound Id'] == c_id_entry]['% Inhibition (HDAC6)'].values[0].item()

        #Create species for each chemical tested
        create_species(model, s_id = cas_num,
                           compartment = 'Brain',
                           constant = False, initial_amount = initial_amount,
                           substance_units = 'dimensionless',
                           boundary_condition = False,
                           has_only_substance_units = False)

        # Modify reaction rate we know is effected in the assays (HDAC6)
        try:
            model.getParameter('parameter_BEL_import_HGNC_HDAC6_increases_BEL_import_GO_Hsp90_deacetylation').setValue(assay_df.loc[assay_df['Compound Id'] == c_id_entry]['% Inhibition (HDAC6)'].values[0].item())
        except:
            pass
        #Create new SBML file for each intervention
        intervention_directory = os.path.join(os.getcwd(),'intervention_SBML_files')
        SBML_file_write_location = os.path.join(intervention_directory,cas_num+'.sbml')

        #Remove file if it already exists
        if os.path.isfile(SBML_file_write_location):
            os.remove(SBML_file_write_location)

        #Write file
        libsbml.writeSBMLToFile(SBML_document, SBML_file_write_location)

def get_uniprot_from_bel(bel):
    BASE = 'http://rest.genenames.org/fetch/symbol/'
    hgnc_symbol = bel.split("\"")[1] #parse for HGNC code
    result2 = requests.get(BASE + hgnc_symbol, headers={ "Accept" : "application/json"})
    try:
        uni_prot_id = result2.json()['response']['docs'][0]['uniprot_ids'][0]
    except:
        uni_prot_id = None
    return uni_prot_id

def bel_relation_type_to_reaction_kinetics(subject, obj, relation_type):
    '''
    returns reactants and products, as lists,
    when given a bel subject, object, and relation type
    (e.g. 'increases','decreases', etc.)
    '''
    if relation_type == 'increases':
        # Reactants --> Products
        # subject   --> subject + object

        reactants=[(1,subject)]
        products=[(1,subject),(1,obj)]

    elif relation_type == 'decreases':
        # Reactants        --> Products
        # subject + object --> subject

        reactants=[(1,subject),(1,obj)]
        products=[(1,subject)]

    return reactants,products

def create_reaction_id(reactants,products):
    reactant_id = ""
    for i, reactant in enumerate(reactants):
        if i > 0:
            reactant_id+="_and_"
        reactant_id+= reactant[1]

    product_id = ""
    for i,product in enumerate(products):
        if i > 0:
            product_id+="_and_"
        product_id+= product[1]

    return reactant_id+"_becomes_"+product_id


# ### BioModels SBML doc. Download

# In[9]:


def get_biomodels_SBML_doc(url, SBML_file_location):
    '''
    brad, todo: write docs.
    '''
    print("Biomodels API request underway for: " + str(url))
    urllib.request.urlretrieve(url, SBML_file_location)
    document = libsbml.readSBMLFromFile(SBML_file_location)
    return document


# ### Controlled Vocabulary Term Generation

# ####  API calls

# In[10]:


def uniprot_to_gene(uniprot_ids):

    print("Uniprot API request underway...")
    url = 'https://www.uniprot.org/uploadlists/'
    params = {'from': 'ACC+ID','to': 'GENENAME','format': 'tab','query': uniprot_ids}
    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as f: response = f.read()

    return response

def bel_node_list_to_hgnc_ids(bel_nodes):

        gene_names = list(filter(None,[entity.split("HGNC")[1].split("\"")[1] if "HGNC" in entity else "" for entity in bel_nodes]))
        query = "+OR+".join(gene if gene else "" for gene in set(gene_names))
        print("HGNC API request underway for the following gene names:")
        print(query)
        response = requests.get(
            'http://rest.genenames.org/search/symbol/'+query,
            headers={'Accept': 'application/json'}
        )

        return pd.json_normalize(response.json()['response']['docs'])

def hgnc_id_to_uniprot(hgnc_ids):

    hgnc_ids = " ".join(hgnc_id for hgnc_id in hgnc_ids)
    print("Uniprot API request underway for the following hgnc_ids:")
    print(hgnc_ids)
    url = 'https://www.uniprot.org/uploadlists/'
    params = {'from': 'HGNC_ID','to': 'ACC','format': 'tab','query': hgnc_ids}
    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as f: response = f.read()
    return {pair.split("\t")[0]:pair.split("\t")[1] for pair in response.decode("utf-8").split("\n")[1:-1] if re.match(".+\t(P|Q).+",pair)}

def get_uniprot_list(df,hgnc_id_to_uniprot_lookup):
    return [hgnc_id_to_uniprot_lookup[row.hgnc_id] if row.hgnc_id in hgnc_id_to_uniprot_lookup else None for index, row in df.iterrows()]

def get_bel_cv_df(bel_df):
    #subject
    subject_bels = bel_df['out'].to_list()
    bel_subject_cv_terms_df = bel_node_list_to_hgnc_ids(subject_bels)
    hgnc_id_to_uniprot_lookup = hgnc_id_to_uniprot(bel_subject_cv_terms_df.hgnc_id)
    uniprot_list = get_uniprot_list(bel_subject_cv_terms_df,hgnc_id_to_uniprot_lookup)
    bel_subject_cv_terms_df['uniprot_ids'] = uniprot_list
    #object
    object_bels = bel_df['in'].to_list()
    bel_object_cv_terms_df = bel_node_list_to_hgnc_ids(object_bels)
    hgnc_id_to_uniprot_lookup = hgnc_id_to_uniprot(bel_object_cv_terms_df.hgnc_id)
    uniprot_list = get_uniprot_list(bel_object_cv_terms_df,hgnc_id_to_uniprot_lookup)
    uniprot_list
    bel_object_cv_terms_df['uniprot_ids'] = uniprot_list
    bel_df['subject_uniprots'] = get_uniprot_ids(bel_df['out'], bel_subject_cv_terms_df)[0] * len(bel_df.index) #todo, fix this?
    bel_df['object_uniprots'] = get_uniprot_ids(bel_df['in'], bel_object_cv_terms_df)

    return bel_df

def get_uniprot_ids(bel_series, bel_cv_df):
    x = pd.DataFrame([])
    for obj in bel_series:
        y = [symbol if symbol in obj else False for symbol in bel_cv_df.symbol]
        x[obj] = y
    all_uniprot_ids = []
    for obj in x:
        for row in x[obj]:
            uniprot_ids = list(bel_cv_df.loc[bel_cv_df.symbol == row].uniprot_ids.values[0] if row else '' for row in x[obj])
            uniprot_ids = list(filter(None, uniprot_ids))
        all_uniprot_ids.append(tuple(uniprot_ids))
    all_uniprot_ids = tuple(uniprot_id for uniprot_id in all_uniprot_ids)
    return all_uniprot_ids


# ####  SBML Model Gene Name Retrieval

# In[11]:


def multi_replace(replacement,string, chars = "[]\',()"):
    for char in chars:
        string = string.replace(char, replacement)
    return string

def get_model_species_cv_df(sbml_model):
    # Get the controlled vocabulary terms of all species in the simulation
    cv_df = pd.DataFrame({
        'element_reference':[subject_species.getId() for subject_species in sbml_model.getListOfSpecies()],\
        'cv_ids':[ tuple(cv_term.getResourceURI(0).split('/')[-1] for cv_term in subject_species.getCVTerms())\
                                    for subject_species in sbml_model.getListOfSpecies()]
    })

    all_model_uniprots = list(filter(None, [cv_id if ":" not in cv_id else None for cv_id in cv_df.cv_ids.unique().tolist()]))

    all_model_uniprots_str = multi_replace("",str(all_model_uniprots),"[]\',()")

    uniprot_response = uniprot_to_gene(all_model_uniprots_str)

    uni_gene_pairs = [(uni_gene_pair.split("\t")[0],uni_gene_pair.split("\t")[1]) for uni_gene_pair in uniprot_response.decode('utf-8').split("\n")[1:-1]]
    uniprot_to_gene_name_lookup = {key:value for (key,value) in uni_gene_pairs}

    all_gene_names=[]
    for cv_id_group in cv_df['cv_ids']:
        groups_gene_names = []
        for cv_id in cv_id_group:
            if ":" not in cv_id and (cv_id[0] == "P" or cv_id[0] == "Q"):
                groups_gene_names.append(uniprot_to_gene_name_lookup[cv_id])
            else:
                pass
        all_gene_names.append(" ".join(groups_gene_names))
    cv_df['gene_names'] = all_gene_names

    return cv_df


# ### Julia

# ### Mega Function

# In[12]:

# from BELtoSBML_test import extend_model
#  extend_model.extend_model(SBML_url = "https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000542.3?filename=BIOMD0000000542_url.xml", SBML_file_location = "doyle_tau.xml", bel_subject_object_pair=[('HDAC6','CDC37')])
def extend_model(auth = dict(),
                SBML_url = "https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000542.3?filename=BIOMD0000000542_url.xml",
                SBML_file_location = "doyle_tau.xml" ,
                bel_subject_object_pair = [('HDAC6','CDC37')],
                initial_amount_subject = 1,
                initial_amount_object = 1,
                reaction_rate = 1.0):
    """
    Extends the species and reactions of a given SBML file with BEL edges selected by HGNC name
    :param auth: Dictionary of authentification details
    :param SBML_url: url String for where to directly download SBML file
    :param SBML_file_location: local path String location of where to download SBML file
    :param bel_subject_object_pair A list of String tuples. Each tuple contains
        one or more gene names for a given interaction, e.g. [('HDAC6','CDC37')]
    :param initial_amount_subject: Starting concentration or quantitty for the BEL subject:
        ['Subject','Object']
    :param initial_amount_object: Starting concentration or quantitty for the BEL object:
        ['Subject','Object']
    :param reaction_rate: Rate of the reaction
    """
    doc = get_biomodels_SBML_doc(SBML_url, SBML_file_location)
    sbml_model = doc.getModel()
    for edge in bel_subject_object_pair:
        print('BEL API request underway for: '+ str(edge))
        out_node,in_node = edge[0],edge[1]
        if in_node and out_node:
            bel_df = retrieve_bel_edges_rest(auth = auth, out_node=out_node, in_node=in_node)
        elif out_node:
            bel_df = retrieve_bel_edges_rest(auth = auth, out_node=out_node)
        else:
            bel_df = retrieve_bel_edges_rest(auth = auth, in_node=in_node)

        print("Here are the results of your query:")
        print(tabulate(bel_df.drop(['annotation'], axis=1),headers='keys', tablefmt='psql'))
        bel_df = get_bel_cv_df(bel_df)
        sbml_cv_df = get_model_species_cv_df(sbml_model)
        print("Adding the following BEL edges:")
        print(tabulate(bel_df.drop(['annotation'], axis=1),headers='keys', tablefmt='psql'))
        print("to your quantitative simulation, containing the following species:")
        print(tabulate(sbml_cv_df,headers='keys', tablefmt='psql'))
        sbml_model = add_bel_df_to_SBML_doc(bel_df, sbml_cv_df, sbml_model,initial_amount_subject, initial_amount_object, reaction_rate)

    # Select write location and file name
    BEL_added_directory = os.path.join(os.getcwd())
    BEL_added_SBML_file_name ="BEL_added"
    SBML_file_write_location = os.path.join(BEL_added_directory,BEL_added_SBML_file_name+".sbml")


    # Remove file if it already exists
    if os.path.isfile(SBML_file_write_location):
        os.remove(SBML_file_write_location)

    # Write to file
    libsbml.writeSBMLToFile(doc, SBML_file_write_location)
    print("\nA new SBMl file has been generated: ", SBML_file_write_location)

    # Check if valid SBML document has been generated
    for error_i in range(0,doc.getNumErrors()):
        if doc.getError(error_i).isWarning():
            continue
        else:
            print("Error writing the SBML file:")
            print("Error type: ", doc.getError(0).getCategoryAsString())
            print(doc.getError(0).getLine())
            print("Error message: ", doc.getError(0).getMessage())
