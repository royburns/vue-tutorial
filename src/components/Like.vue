<template>
    <div>
        <a class="btn btn-default btn-sm" @click="time()">
            <i class="fa fa-cog"></i> Settings</a>
        <p>ABC</p>
    </div>
</template>

<script>
    export default{
        methods: {
            time(){

                    this.$store.dispatch('addTotalTime', 1)

            }
        }
    }
</script>
