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
        state.mpList.push(
            // TODO: add subscribe time
            Object.assign(mp)
        )
    },
    // 删除某公众号
    [types.UNSUBSCRIBE_MP] (state, idx) {
        state.mpList.splice(idx, 1);
    }
};