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
    unsubscribeMp({ commit }, weixinhao) {
        commit(types.UNSUBSCRIBE_MP, weixinhao)
    },
    addSearchResultList({ commit }, mp) {
        commit(types.ADD_SEARCHRESULT_LIST, mp)
    },
    unsubSearchResult({ commit }, weixinhao) {
        commit(types.UNSUBSCRIBE_SEARCHRESULT, weixinhao)
    },
    clearSearchResult({ commit }, info) {
        commit(types.CLEAR_SEARCHRESULT, info)
    },
    	initFromLS({ commit }, info) {
        commit(types.INIT_FROM_LS, info)
    }

}