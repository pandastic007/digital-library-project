<template>
  <div>
    <el-result icon="warning" title="Warning" sub-title="404 Not Found">
      <template #extra>
        <el-button type="primary" @click="$router.push('/')">Back</el-button>
      </template>
    </el-result>
  </div>
</template>
