<template>
  <div id="app">
    <div class="main-container">
      <div class="sidebar">
        <h2>Структура подразделений</h2>
        <div class="button-container">
          <button type="primary" @click="openCreateDivisionModal" class="add-button">
            <img src="@/assets/plus.svg" alt="Добавить" class="button-icon" />
            Добавить
          </button>
        </div>
        <DivisionTree 
          ref="divisionTree" 
          :selectedId="selectedDivisionId"
          @division-selected="updateSelectedDivision" 
          @save="handleSaveDivision" 
        />
      </div>
      <div class="content">
        <h1 class="division-title">Подразделения и сотрудники</h1>
        <h2 class="statistics-title">Статистика подразделения</h2>
        <div>
          <EmployeeList v-if="selectedDivisionId" :divisionId="selectedDivisionId" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import './App.css';
import DivisionTree from './components/DivisionTree.vue';
import EmployeeList from './components/EmployeeList.vue';

export default {
  name: 'App',
  components: {
    DivisionTree,
    EmployeeList,
  },
  data() {
    return {
      selectedDivisionId: null
    };
  },
  methods: {
    updateSelectedDivision(id) {
      this.selectedDivisionId = id;
    },
    openCreateDivisionModal() {
      this.$refs.divisionTree.openEditModal();
    },
    handleSaveDivision(newDivision) {
      if (this.$refs.divisionTree) {
        this.$refs.divisionTree.addDivisionToTree(newDivision);
      }
    }
  }
};
</script>