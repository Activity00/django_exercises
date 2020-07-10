import logging
import time

from django_redis import get_redis_connection

from rest_framework.response import Response
from rest_framework.views import APIView

from ranking.serializers import RankingSerializer, RankingGetSerializer
from ranking import const


log = logging.getLogger('ranking')


class RankingView(APIView):

    def get(self, request):
        """获取排行榜"""
        serializer = RankingGetSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(data={'status': 400, 'message': 'params error', 'data': serializer.errors})

        start = serializer.data['start'] - 1
        end = serializer.data['end']
        device_id = serializer.data['device_id']

        # 获取排名
        conn = get_redis_connection()
        try:
            device_score = conn.zrevrange(const.RK_RANKING, start, end, withscores=True, score_cast_func=float)
        except Exception as e:
            log.error(f'RankingView get zrange error: {e!r}')
            return Response(data={'status': 500, 'message': 'internal error'})

        # 组织返回
        data = []
        own = None
        rank_start = serializer.data['start']
        for dt in device_score:
            info = {'ranking': rank_start, 'device_id': dt[0].decode(), 'score': int(dt[1])}
            data.append(info)
            rank_start += 1

            if dt[0].decode() == device_id:
                own = info
        if own:
            data.append(own)
        else:
            # 当自己不再区间时候获取自己的相关信息
            try:
                own_score = conn.zscore(const.RK_RANKING, device_id)
            except Exception as e:
                log.error(f'RankingView get zscore error: {e!r}')
                own_score = None

            if own_score and own_score > 0:
                try:
                    own_rank = conn.zrevrank(const.RK_RANKING, device_id)
                except Exception as e:
                    log.error(f'RankingView get zscore error: {e!r}')
                else:
                    data.append({'ranking': own_rank + 1, 'device_id': device_id, 'score': own_score})

        return Response(data={'status': 0, 'message': 'OK', 'data': data})

    def post(self, request):
        """提交分数"""
        serializer = RankingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'status': 400, 'message': 'params error', 'data': serializer.errors})

        conn = get_redis_connection()
        try:
            conn.zadd(const.RK_RANKING, {serializer.data['device_id']: serializer.data['score']})
        except Exception as e:
            log.error(f'RankingView post zadd error: {e!r}, data: {serializer.data!r}')
            return Response(data={'status': 500, 'message': 'internal error'})

        return Response(data={'status': 0, 'message': 'OK'})
