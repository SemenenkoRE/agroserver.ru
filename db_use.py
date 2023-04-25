from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_create import AgroserverTechnic
from sqlalchemy import desc
import datetime


class SqlAddAgroserverTechnic:

    """  """

    engine = create_engine("mysql+pymysql://root:111111@localhost/data_base_agroserver", echo=True)

    def __init__(self, **kwargs):
        self.filling_data(kwargs)

    def filling_data(self, values_collection):
        session = sessionmaker(bind=self.engine)
        session = session()
        session.add(AgroserverTechnic(id=values_collection['id'],
                                            hex_id=values_collection['hex_id'],
                                            reference_ad=values_collection['reference_ad'],
                                            header_ad=values_collection['header_ad'],
                                            type_technic=values_collection['type_technic'],
                                            price_alone=values_collection['price_alone'],
                                            price_lower=values_collection['price_lower'],
                                            price_upper=values_collection['price_upper'],
                                            price_unit=values_collection['price_unit'],
                                            offer_datetime=values_collection['offer_datetime'],
                                            address=values_collection['address'],
                                            model_technic=values_collection['model_technic'],
                                            year=values_collection['year'],
                                            condition=values_collection['condition'],
                                            maker=values_collection['maker'],
                                            moto_hours=values_collection['moto_hours'],
                                            power_engine=values_collection['power_engine'],
                                            traktor_base=values_collection['traktor_base']))

        session.commit()


class SqlDataBaseQuery:

    """  """

    engine = create_engine("mysql+pymysql://root:111111@localhost/data_base_agroserver", echo=True)

    def __init__(self):
        self.session = sessionmaker(bind=self.engine)
        self.session = self.session()

#     def query_get_all(self):
#
#         """
#         Получение всех сведений сведений из базы данных
#         """
#
#         result = self.session.query(AvitoTechnic).all()
#
#         for row in result:
#             print("Id: ", row.id, "\nhex_id: ", row.hex_id, "\nreference_ad: ", row.reference_ad,
#                   "\ntitle_text: ", row.title_text, "\ntype_technic: ", row.type_technic, "\nprice: ", row.price,
#                   "\noffer_datetime: ", row.offer_datetime, "\naddress: ", row.address, "\narea: ", row.area,
#                   "\nmodel_request: ", row.model_request, "\nmodel_research: ", row.model_research,
#                   "\nmodel_exact: ", row.model_exact, "\nyear: ", row.year, "\ncondition: ", row.condition,
#                   "\nmaker: ", row.maker, "\nmaker_request: ", row.maker_request, "\nmoto_hours: ", row.moto_hours,
#                   "\ndocument: ", row.document, "\n************")
#
#
#     def query_get_data_id(self, research_id):
#
#         """
#         Получение сведений о коллекции определенного id.
#         """
#
#         result = self.session.query(AvitoTechnic).all()
#
#         for row in result:
#             if row.id == research_id:
#                 print("Id: ", row.id, "\nhex_id: ", row.hex_id, "\nreference_ad: ", row.reference_ad,
#                       "\ntitle_text: ", row.title_text, "\ntype_technic: ", row.type_technic, "\nprice: ", row.price,
#                       "\noffer_datetime: ", row.offer_datetime, "\naddress: ", row.address, "\narea: ", row.area,
#                       "\nmodel_request: ", row.model_request, "\nmodel_research: ", row.model_research,
#                       "\nmodel_exact: ", row.model_exact, "\nyear: ", row.year, "\ncondition: ", row.condition,
#                       "\nmaker: ", row.maker, "\nmaker_request: ", row.maker_request, "\nmoto_hours: ", row.moto_hours,
#                       "\ndocument: ", row.document, "\n************")

    def query_delete_row(self, research_id):

        """ """

        result = self.session.query(AgroserverTechnic).all()

        for row in result:
            if row.id == research_id:
                self.session.delete(row)
                self.session.commit()


    def query_last_id(self):

        """ Получение унркального id для добавляемой строки """

        last_id = None
        result = self.session.query(AgroserverTechnic).order_by(desc(AgroserverTechnic.id))

        for row in result:
            last_id = row.id + 1
            break

        return last_id


if __name__ == '__main__':

    sql_query = SqlDataBaseQuery()
    # sql_query.query_get_all()
    # sql_query.query_get_data_id(45)
    sql_query.query_delete_row(1)
    # print(sql_query.query_get_last_id())

    pass

