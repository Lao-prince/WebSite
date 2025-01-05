<template>
  <div class="division-tree">
    <ul>
      <DivisionItem
        v-for="division in divisions"
        :key="division.id"
        :division="division"
        :selected-id="selectedDivisionId"
        :selected-parent-ids="selectedParentIds"
        @update-name="updateDivisionName"
        @select="selectDivision"
        @toggle="toggleDivision(division)"
        @delete="deleteDivision"
      />
    </ul>
    <EditDivisionModal
      :visible="showEditModal"
      :division="selectedDivision"
      :allDivisions="getAllDivisions()"
      @close="showEditModal = false"
      @save="addDivisionToTree"
    />
  </div>
</template>

<script>
import './Division.css';
import DivisionItem from './DivisionItem.vue';
import EditDivisionModal from './EditDivisionModal.vue';
import axios from 'axios';

export default {
  name: 'DivisionTree',
  components: { DivisionItem, EditDivisionModal },
  data() {
    return {
      divisions: [],
      showEditModal: false,
      selectedDivision: {},
      selectedDivisionId: null, 
      selectedParentIds: [], 
    };
  },
  methods: {
    async fetchDivisions() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/divisions/');
        this.divisions = this.buildHierarchy(response.data);
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
      }
    },
    buildHierarchy(divisions) {
      const map = {};
      const roots = [];
      divisions.forEach((division) => {
        map[division.id] = { ...division, children: [] };
      });

      divisions.forEach((division) => {
        if (division.parent === null) {
          roots.push(map[division.id]);
        } else {
          if (map[division.parent]) {
            map[division.parent].children.push(map[division.id]);
          }
        }
      });

      return roots;
    },
    getAllDivisions() {
      const collectAllDivisions = (divisions) => {
        return divisions.reduce((acc, division) => {
          acc.push({ id: division.id, name: division.name });
          if (division.children) {
            acc = acc.concat(collectAllDivisions(division.children));
          }
          return acc;
        }, []);
      };
      return collectAllDivisions(this.divisions);
    },
    openEditModal() {
      this.showEditModal = true;
      this.selectedDivision = { id: null, name: '', parent: null };
    },
    async addDivisionToTree(newDivision) {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/divisions/', {
          name: newDivision.name,
          parent: newDivision.parent,
        });

        const savedDivision = response.data;
        const divisionWithChildren = {
          id: savedDivision.id,
          name: savedDivision.name,
          parent: savedDivision.parent,
        };

        if (!savedDivision.parent) {
          this.divisions.push(divisionWithChildren);
        } else {
          const addRecursively = (divisions) => {
            for (let division of divisions) {
              if (division.id === savedDivision.parent) {
                if (!division.children) division.children = [];
                division.children.push(divisionWithChildren);
                return true;
              }
              if (division.children && addRecursively(division.children)) return true;
            }
            return false;
          };
          addRecursively(this.divisions);
        }

        this.showEditModal = false;
      } catch (error) {
        console.error('Ошибка при добавлении нового подразделения:', error);
        this.$message.error('Не удалось добавить подразделение');
      }
    },
    toggleDivision(division) {
      division.expanded = !division.expanded;
    },
    selectDivision(id) {
      this.selectedDivision = this.divisions.find(division => division.id === id);
      this.selectedDivisionId = id;
      this.selectedParentIds = this.getParentIds(id); 
      this.$emit('division-selected', id);
    },
    getParentIds(id) {
      const parentIds = [];
      const findParent = (divisions, targetId) => {
        for (const division of divisions) {
          if (division.children) {
            if (division.children.some((child) => child.id === targetId)) {
              parentIds.push(division.id);
              findParent(this.divisions, division.id);
            } else {
              findParent(division.children, targetId);
            }
          }
        }
      };
      findParent(this.divisions, id);
      return parentIds;
    },
    async updateDivisionName({ id, name }) {
      try {
        // Обновлtybt названиz в интерфейсе
        const updateNameRecursively = (divisions) => {
          for (let division of divisions) {
            if (division.id === id) {
              division.name = name;
              return true;
            }
            if (division.children) {
              const found = updateNameRecursively(division.children);
              if (found) return true;
            }
          }
          return false;
        };
        updateNameRecursively(this.divisions);

        await axios.put(`http://127.0.0.1:8000/api/divisions/${id}/`, { name });
      } catch (error) {
        console.error('Ошибка при обновлении названия подразделения:', error);
        this.$message.error('Не удалось сохранить изменения на сервере');
      }
    },
    async deleteDivision(id) {
      try {
        await axios.delete(`http://127.0.0.1:8000/api/divisions/${id}/`);
        const deleteRecursively = (divisions) => {
          for (let i = 0; i < divisions.length; i++) {
            if (divisions[i].id === id) {
              divisions.splice(i, 1);
              return true;
            }
            if (divisions[i].children) {
              const found = deleteRecursively(divisions[i].children);
              if (found) {
                if (divisions[i].children.length === 0) {
                  divisions[i].children = null;
                }
                return true;
              }
            }
          }
          return false;
        };
        deleteRecursively(this.divisions);
      } catch (error) {
        console.error(`Ошибка при удалении элемента с ID ${id}:`, error);
      }
    },
  },
  mounted() {
    this.fetchDivisions();
  },
};
</script>
