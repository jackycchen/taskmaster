<template>
  <el-form :model="form" label-width="80px">
    <el-form-item label="标题" required>
      <el-input v-model="form.title" />
    </el-form-item>
    <el-form-item label="描述">
      <el-input v-model="form.description" type="textarea" />
    </el-form-item>
    <el-form-item label="截止时间">
      <el-date-picker
        v-model="form.due_date"
        type="datetime"
        placeholder="选择日期时间"
        format="YYYY-MM-DD HH:mm"
        value-format="YYYY-MM-DDTHH:mm:ss"
      />
    </el-form-item>
    <el-form-item label="优先级">
      <el-select v-model="form.priority" placeholder="请选择">
        <el-option label="高" :value="1" />
        <el-option label="中" :value="2" />
        <el-option label="低" :value="3" />
      </el-select>
    </el-form-item>
    <el-form-item label="状态">
      <el-select v-model="form.status" placeholder="请选择">
        <el-option label="待办" value="pending" />
        <el-option label="进行中" value="in_progress" />
        <el-option label="已完成" value="completed" />
      </el-select>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="handleSubmit">提交</el-button>
      <el-button @click="$emit('cancel')">取消</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { reactive, watch } from 'vue'

export default {
  name: 'TaskForm',
  props: {
    task: {
      type: Object,
      default: null
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const form = reactive({
      title: '',
      description: '',
      due_date: '',
      priority: 2,
      status: 'pending'
    })

    watch(() => props.task, (newTask) => {
      if (newTask) {
        form.title = newTask.title
        form.description = newTask.description
        form.due_date = newTask.due_date
        form.priority = newTask.priority
        form.status = newTask.status
      } else {
        form.title = ''
        form.description = ''
        form.due_date = ''
        form.priority = 2
        form.status = 'pending'
      }
    }, { immediate: true })

    const handleSubmit = () => {
      emit('submit', { ...form })
    }

    return {
      form,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.el-form {
  padding: 20px;
}
</style>