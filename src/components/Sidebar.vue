<template>
    <div>
  <div class="panel panel-default">
    <div class="panel-heading">
      <h1 class="text-center">
        <span class="fa-stack fa-2x">
  <i class="fa fa-square-o fa-stack-2x"></i>
  <i class="fa fa-flag fa-stack-1x"></i>
</span>
        已有时长</h1>
      <span class="fa-stack fa-2x" style="color: red;">
  <i class="fa fa-circle fa-stack-2x"></i>
  <i class="fa fa-heart fa-stack-1x fa-inverse"></i>
</span>
    </div>

    <div class="panel-body">
      <h1 class="text-center">{{ time }} 小时</h1>
    </div>

  </div>
        <!--<hr>-->
    <!--<router-view></router-view>-->
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