from astock import tradeService
import requests
ts = tradeService.tradeService('800200')
ts.syncAccount({'a':'bb'})