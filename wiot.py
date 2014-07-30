import pandas as pd
import numpy as np

class world_input_output_table:
    def initialise(self):
        #%%
        # Import csv
        wiot = pd.read_csv("wiot_2010.csv", true_values='t', false_values='f')
        wiot = wiot.set_index(
            ['from_iso3', 'from_sector_id', 'to_iso3', 'to_sector_id']).sortlevel()
        
        #%%
        # Gross output (total production), x
        tot_prod = wiot['flow_amount'].sum(level=['from_iso3', 'from_sector_id'])
        
        #%%
        # The intermediates matrix, Z (41 x 35) x (41 x 35)
        sector_flows = wiot[
            ~wiot.is_final_demand & ~wiot.is_investment & ~wiot.is_value_added]
        sector_flows = sector_flows['flow_amount']
        sector_flows = sector_flows.unstack(['to_iso3', 'to_sector_id'])
        
        #%%
        # The total final demand vector (41 x 35)
        final_demand = wiot[wiot.is_final_demand]
        final_demand = final_demand.groupby(
            level=['from_iso3', 'from_sector_id'])['flow_amount'].sum()
        
        #%%
        # Investments
        investments = wiot[wiot.is_investment]
        investments = investments.groupby(
            level=['from_iso3', 'from_sector_id'])['flow_amount'].sum()
            
        #%%
        # Convert B to coefficients (divide by gross output)
        tech_coefs = sector_flows.div(tot_prod, axis='columns')
        
        #%%
        # Remove any sectors which have 0 total production:
        no_production = tot_prod[tot_prod == 0]
        tot_prod = tot_prod[tot_prod > 0]
        sector_flows = sector_flows.drop(no_production.index.values, axis=1) \
            .drop(no_production.index.values, axis=0)
        final_demand = final_demand.drop(no_production.index.values)
        tech_coefs = tech_coefs.drop(no_production.index.values, axis=1) \
            .drop(no_production.index.values, axis=0)
        investments = investments.drop(no_production.index.values)
        
        #%%
        # The identity matrix, I
        ident = np.eye(final_demand.shape[0])
        
        self.final_demand = final_demand
        self.tech_coefs = tech_coefs
        self.investments = investments
        self.ident = ident
        
    def total_production(self, final_demand=None):
        if final_demand is None:
            final_demand = self.final_demand
        #%%
        # x = Ax + f + n=> x = (I - A)^-1.(f + n)
        # Solve for Q
        i = self.ident
        a = self.tech_coefs
        f = self.final_demand
        n = self.investments
        tot_prod = np.linalg.solve(i - a, f + n)
        return pd.Series(tot_prod, index=final_demand.index)
        
wiot = world_input_output_table()
wiot.initialise()