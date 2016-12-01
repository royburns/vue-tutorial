<template>
  <div>
  <div class="jumbotron">
    <h1>任务追踪</h1>
    <p>
      <strong>
        <router-link to="/time-entries">创建一个任务</router-link>
      </strong>
    </p>
  </div>
  <router-link
          to="/home/like"
          class="btn btn-primary">
    <i class="fa fa-cog"></i> 喜欢 {{ time }}
  </router-link>

    <router-view></router-view>
  <hr>


  </div>
</template>

<script>
    export default {
        computed: {
            time() {
                return this.$store.state.totalTime
            }
        }
    }
</script>