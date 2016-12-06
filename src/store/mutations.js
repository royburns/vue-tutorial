import * as types from './mutation-types'

export default {
    // 增加总时间
    [types.ADD_TOTAL_TIME] (state, time) {
        state.totalTime = state.totalTime + time
    },
    // 减少总时间
    [types.DEC_TOTAL_TIME] (state, time) {
        state.totalTime = state.totalTime - time
    },
    // 新增计划
    [types.SAVE_PLAN] (state, plan) {
        // 设置默认值，未来我们可以做登入直接读取昵称和头像
        const avatar = 'https://sfault-avatar.b0.upaiyun.com/147/223/147223148-573297d0913c5_huge256';

        state.list.push(
            // Object.assign({ name: '二哲', avatar: avatar }, plan)
            Object.assign(plan)
        )
    },
    // 删除某计划
    [types.DELETE_PLAN] (state, idx) {
        state.list.splice(idx, 1);
    },
    // 订阅某公众号
    [types.SUBSCRIBE_MP] (state, mp) {
        state.subscribeList.push(
            // TODO: add subscribe time
            Object.assign(mp)
        )
        for(let item of state.mpList) {
            if(item.weixinhao == mp.weixinhao) {
                var idx = state.mpList.indexOf(item);
                state.mpList[idx].isSubscribed = true;
                break;
            }
        }
    },
    // 删除某公众号
    [types.UNSUBSCRIBE_MP] (state, weixinhao) {
        for(let item of state.mpList) {
            if(item.weixinhao == weixinhao) {
                var idx = state.mpList.indexOf(item);
                state.mpList[idx].isSubscribed = false;
                break;
            }
        }

        for(let item of state.subscribeList) {
            if(item.weixinhao == weixinhao) {
                var idx = state.subscribeList.indexOf(item);
                console.log('unscrib:'+idx);
                break;
            }
        }

        state.subscribeList.splice(idx, 1);
    },
    [types.ADD_SEARCHRESULT_LIST] (state, mps) {
        state.mpList = state.mpList.concat(mps);
    },
    [types.UNSUBSCRIBE_SEARCHRESULT] (state, weixinhao) {
        for(let item of state.mpList) {
            if(item.weixinhao == weixinhao) {
                var idx = state.mpList.indexOf(item);
                state.mpList[idx].isSubscribed = false;
                break;
            }
        }
        for(let item of state.subscribeList) {
            if(item.weixinhao == weixinhao) {
                var idx = state.subscribeList.indexOf(item);
                console.log('unscrib:'+idx);
                break;
            }
        }
        state.subscribeList.splice(idx, 1);
    },
    [types.CLEAR_SEARCHRESULT] (state, info) {
        console.log('clear search result:' + info);
        state.mpList = [];
    }

};