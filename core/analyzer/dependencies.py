from core.analyzer.repository import AnalyzerRepository
from core.analyzer.service import AnalyzerService
from core.gigachat.service import GigachatService
from core.moex.service import MoexService


def get_moex_service() -> MoexService:
    return MoexService(AnalyzerRepository())


def get_analyzer_service() -> AnalyzerService:
    moex_service = get_moex_service()
    return AnalyzerService(GigachatService(), moex_service, moex_service.repository)
