import xmlrpc.client

class OdooConnection:
    
    def __init__(self, url, db, user, key):
        """_summary_

        Args:
            url (_str_): 
            db (_str_): 
            user (_str_): 
            key (_str_): 
            
            The xmlrpc/2/common endpoint provides meta-calls which don’t require authentication, 
            such as the authentication itself or fetching version information. 
            To verify if the connection information is correct before trying to authenticate, 
            the simplest call is to ask for the server’s version. 
            The authentication itself is done through the authenticate function and returns a user identifier (uid) used in authenticated calls instead of the login.
        """
        self.url = url
        self.db = db
        self.user = user
        self.key = key
        
        self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        self.uid = self.common.authenticate(self.db, self.user, self.key , {})

        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')

    def state(self):
        if self.uid :
            return f'connected using uid : {self.uid}\n'
        else :
            return f'Authentication failed for uid :for uid : {self.uid}\n'

    def call_method (self, model, method  , args = [] ,kwargs = {}):
        
        """_Execute a method in the model passed on an odoo server. _
            
            Takes in a method to execute and then  `ids` as a list of ids .  
            Beginning with a list of ids followed by any arguments.
            
            Note: The method you are trying to call must be public  
            and should return a value.

        Args:
            model (_str_): _model_name_
            method (_str_): _method_name_
            args (list/array): list of parameters passed by position . Defaults to [].
            kwargs (dict, optional): mapping dict of parameters to pass by keyword . Defaults to {}.    
                        
            Example:

            call_method(    
                    model, 
                    method, 
                    args = [[list of ids], arg1, arg2...], kwargs = {key: value} 
                        )
            
        Returns:
            Depends on the method you calling
        
        """

        ret = self.models.execute_kw(self.db, self.uid, self.key, model, method ,args , kwargs)
        if ret :
            return ret 
        else :
            return False

    def check_access_right (self, model, access_right = 'read'):
        """_this method allow us to check the access right of a given user on a given model_

        Args:
            model (_str_): _model_name_
            access_right (_str_): Defaults to 'read'.
            access_right = 'read' || 'create' || 'write' || 'unlink' 
        Returns:
            _type_: _description_
        """
        return self.call_method(model,'check_access_rights',[access_right] ,{'raise_exception': False})
        
    
    def get_ids( self, model , query = [], offset = 0, limit = 0 ):
        """_this allow to get the ids of records of a model _

        Args:
            model (_str_): _model_name_
            query (list, optional): query. Defaults to [].
            offset (int, optional): step. Defaults to 0.    
            limit (int, optional): to return a limited number of records .Defaults to 0.
            example : if ids = [8,7,6,5,4,3,2,1] and offset = 5:
                        returned_ids = [3,2,1]
        Returns:
            _array_: _list of ids _
        """
            
        if self.check_access_right(model):
            
            if query != [] and type(query[0])!= list:
                query = [query]

            search_result = self.call_method(model,'search', [query], {'offset': offset, 'limit': limit})
            return search_result
        else: 
            return False
    
    def get_records( self, model, ids, fields =[] ):
        """_this method is used to return records_

        Args:
            model (_str_): model_name 
            ids (_int/array_): the id/ids of the records(s)
            fields (array, optional): fields that u wanna get returned .Defaults to [].

        Returns:
            array : [{'field1':value1, 'field2':value2}] 
        """
        if self.check_access_right(model):
            kwargs = {}
            if fields != {}:
                kwargs =  {'fields':fields}
        
            search_result = self.call_method(model,'read',[ids] , kwargs)
            return search_result
        
        else:
            return False

    # def get_attrs(self, model, ids, ):
    #     pass

    def create(self, model, vals):
        """_summary_

        Args:
            model (string): model_name
            vals (dict/list): a d
            example:    vals = {'field1':'value1','field2' : value2} or 
                        vals = [{'field1':'value1','field2' : value2} , 
                                {'field1':'value3','field2' : value4} ]
                        to create multiple records

        """
        args = [vals]
        ret = self.call_method (model, 'create', args) 
        return ret

    
    def write(self, model, id , vals ):
        """ this method is used to update records.
        Args:
            model (string): model_name
            id (list/array): contains the id of the record that we want to update
            vals_dict (dictionnary): for example vals_dict = { 'field1': 'value1' , 'field2':'value2'}

        """
        args = [id,vals]
        return self.call_method (model, 'write', args)

    def update(self, model, id , vals):
        return self.write (model, id , vals)

    def unlink (self, model, ids):
        
        """ this method is used to delete records.
        Args:
            model (string): model_name
            id (list/array): contains the ids of the records that we want to delete

        """
        args = [ids]
        return self.call_method (model, 'unlink', args)

    
    def delete (self, model, ids):
        return self.unlink(model,ids)



class OdooStockapi(OdooConnection):
    


    def get_stockable_products_ids(self ,query = ['detailed_type','=','product'] ):  
            
        model = 'product.product'
        stockable_products_ids = self.get_ids(model,query)# only stockable products
        return stockable_products_ids
    
    def get_stockable_products_records(self,fields = [] , offset = 0 , limit = 0):
        model = ''
        stockable_products = []
        stockable_products_ids =  self.get_stockable_products_ids()
        
        if stockable_products_ids:
            model = 'product.product'
            stockable_products = self.get_records(model,stockable_products_ids ,fields )
        return stockable_products

    def get_stock_locations(self ,fields = ['id','location_id','product_id','quantity','product_uom_id','company_id'] , offset = 0, limit = 0):
        fields = fields
        model = ''
        internal_location_ids = self.get_internal_locations_ids()
        internal_stock_ids = []
        stock_location = []
        if internal_location_ids:
            model = 'stock.quant'
            internal_stock_ids =  self.get_ids(model,['location_id','in',internal_location_ids],offset,limit)
            # print(fields)
            stock_location = self.get_records(model,internal_stock_ids ,fields)
        return stock_location 
    

    


    def get_internal_locations_ids(self ):
        model = 'stock.location'
        internal_location_ids = self.get_ids(model,['usage','=','internal'])
        return internal_location_ids

    def get_internal_locations_records(self , fields = ['id','display_name', 'company_id'] ):
        model = 'stock.location'
        internal_location_recs = []
        internal_location_ids = self.get_internal_locations_ids()
        if internal_location_ids:
            internal_location_recs = self.get_records(model,internal_location_ids ,fields)
        return internal_location_recs

    def create_product_lot(self,val_dict):
        model = 'stock.production.lot'
        if val_dict:
            self.create(model,val_dict)

    def get_lot_ids(self):
        model = 'stock.production.lot'
        lot_ids = self.get_ids(model)
        return lot_ids

    def get_lot_records(self , fields = ['company_id','display_name' , 'product_id' , 'product_qty',] ):
        model = 'stock.production.lot'
        lot_ids = []
        lot_ids = self.get_lot_ids()
        if lot_ids:
            lot_ids_recs = self.get_records(model,lot_ids ,fields)
        return lot_ids_recs



url = 'http://192.168.1.98:8069'
db = 'bilbao_test_2'
user = 'admin@dzexpert.com'
key = '9691c22a00c554bb26586520ef7f19669583e2d9'

connection = OdooStockapi(url,db,user,key)
# print(connection.get_lot_records()[0])

print(connection.get_stock_locations(fields=[])[0].keys())