from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import openapi
from logger.log_config import CustomLogger

from parsers.api_accruals import accruals_parser
from parsers.api_egov_iin_parser import egov_iin_parser
from parsers.api_elicense_parser import elicense_parser
from parsers.api_goszakup_parser import parse_participant
from parsers.api_payments_parser import api_payments_parser
from parsers.api_adilet_debtors_parser import adilet_debtors_parse
from parsers.api_goszakup_parser import parse_unrelaible_participant
from parsers.api_adilet_opendata_parser import adilet_opendata_parser
from parsers.api_tax_debt_agreement_parser import tax_debt_agreement_parser


app = FastAPI(
    title="Api Parsers",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url = None,
)
app.logger = CustomLogger().set_logger()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(openapi.router)
                    
                       
@app.get("/healthcheck")
def root():
    return {"status": "Api parser is OK!"}


@app.get("/accruals")
def accruals(bin: str):
    ''' Сервис предоставления информации по начислениям 
    на налогоплательщика: земля, имущество, транспорт
    '''
    return accruals_parser(bin)


@app.get("/adilet_debtors")
def adilet_debtors(iin_bin: str):
    ''' Поиск в едином реестре должников и временно ограниченных на 
    выезд должников физических лиц, должностных лиц юридического лица
    '''
    return adilet_debtors_parse(iin_bin)


@app.get("/goszakup")
def goszakup(iin_bin: str):
    ''' Поиск участника госзакупок
    '''
    return parse_participant(iin_bin)


@app.get("/goszakup_unrelaible")
def goszakup_unrelaible(iin_bin: str):
    ''' Поиск недобросовестного участника госзакупок
    '''
    return parse_unrelaible_participant(iin_bin)


@app.get("/payments")
def payments(bin: str, start_date='2010-01-01',):
    ''' Сервис по предоставлению информации об уплаченных 
    суммах на лицевом счете налогоплательщика.
    '''
    return api_payments_parser(bin, start_date,)


@app.get("/tax_debt_agreement")
def tax_debt_agreement(iin_bin: str):
    ''' Сервис по предоставлению информации о налоговой задолженности.
    '''
    return tax_debt_agreement_parser(iin_bin)


@app.get("/adilet_opendata_bin")
def adilet_opendata(bin: str):
    ''' Поиск в едином реестре должников и временно ограниченных на 
    выезд должников физических лиц, должностных лиц юридического лица.
    '''
    return adilet_opendata_parser(bin)


@app.get("/egov_base_iin_info")
def egov_base_iin_info(iin: str):
    ''' Данный физ лица по ИИН 
    '''
    return egov_iin_parser(iin)


@app.get("/elicense")
def elicense(bin: str):
    ''' Получение данных о лицензиях по БИН/ИИН 
    '''
    return elicense_parser(bin)
