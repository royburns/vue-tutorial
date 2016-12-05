import * as types from './mutation-types'

export default {
    addTotalTime({ commit }, time) {
        commit(types.ADD_TOTAL_TIME, time)
    },
    decTotalTime({ commit }, time) {
        commit(types.DEC_TOTAL_TIME, time)
    },
    savePlan({ commit }, plan) {
        commit(types.SAVE_PLAN, plan);
    },
    deletePlan({ commit }, plan) {
        commit(types.DELETE_PLAN, plan)
    },
    subscribeMp({ commit }, mp) {
        commit(types.SUBSCRIBE_MP, mp)
    },
	    unsubscribeMp({ commit }, idx, weixinhao) {
        commit(types.UNSUBSCRIBE_MP, idx, weixinhao)
    }
}