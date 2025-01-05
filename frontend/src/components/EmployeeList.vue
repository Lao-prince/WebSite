<template>
  <div>
    <!-- Раздел статистики -->
    <div v-if="filteredEmployees.length" class="statistics-section">
      <div class="stat-box">
        <p class="stat-title">Количество сотрудников</p>
        <div class="stat-bar"></div>
        <p class="stat-value">{{ employeeCount }} <span>чел.</span></p>
      </div>
      <div class="stat-box">
        <p class="stat-title">Средний возраст</p>
        <div class="stat-bar"></div>
        <p class="stat-value">{{ averageAge }} <span>года</span></p>
      </div>
      <div class="stat-box">
        <p class="stat-title">Средний стаж работы</p>
        <div class="stat-bar"></div>
        <p class="stat-value">{{ averageExperience }} <span>лет</span></p>
      </div>
    </div>

    <div class="info-plus">
      <h2 class="statistics-title">Список сотрудников</h2>
      <button @click="openCreateDivisionModal" class="button-plus">
        Добавить
        <img src="@/assets/plus.svg" alt="Добавить" class="button-plus-icon" />
      </button>
    </div>

    <!-- Раздел списка сотрудников -->
    <div v-if="filteredEmployees.length" class="employee-list-container">
      <div class="employee-header">
        <div class="header-label">ФИО</div>
        <div class="header-label">Должность</div>
        <div class="header-label">Дата рождения</div>
        <div class="header-label">Дата начала работы</div>
      </div>
      <hr class="employee-divider" />
      <div v-for="employee in filteredEmployees" :key="employee.id" class="employee-card">
        <div class="employee-info">
          <img :src="getPhoto(employee.photo)" alt="Фото сотрудника" class="employee-photo" />
          <div class="info-value">{{ employee.full_name }}</div>
          <div class="info-value">{{ employee.position }}</div>
          <div class="info-value">{{ formatDate(employee.birth_date) }}</div>
          <div class="info-value">{{ formatDate(employee.start_date) }}</div>
          <div class="employee-instrument">
            <img src="@/assets/change.svg" alt="Изменить" class="button-plus-icon" @click="openEditDialog(employee)" />
            <span class="delete-icon" @click="openDeleteDialog(employee.id)">✖</span>
          </div>
        </div>
        <hr class="employee-divider" />
      </div>
    </div>

    <div v-else>
      <p>Нет сотрудников в этом подразделении.</p>
    </div>
    <!-- Модальное окно добавления сотрудника -->
    <el-dialog
      :model-value="showCreateDialog"
      title="Добавить сотрудника"
      width="400px"
      @close="closeCreateDialog"
    >
      <el-form :model="newEmployee" label-width="160px">
        <el-form-item label="ФИО">
          <el-input v-model="newEmployee.full_name" />
        </el-form-item>
        <el-form-item label="Должность">
          <el-input v-model="newEmployee.position" />
        </el-form-item>
        <el-form-item label="Дата рождения">
          <el-date-picker
            v-model="newEmployee.birth_date"
            type="date"
            placeholder="Выберите дату"
            format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="Дата начала работы">
          <el-date-picker
            v-model="newEmployee.start_date"
            type="date"
            placeholder="Выберите дату"
            format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="Фото">
          <input type="file" @change="handlePhotoUpload" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="closeCreateDialog">Отмена</el-button>
        <el-button type="primary" @click="createEmployee">Добавить</el-button>
      </template>
    </el-dialog>

    <!-- Модальное окно редактирования сотрудника -->
    <el-dialog
      :model-value="showEditDialog"
      title="Редактировать сотрудника"
      width="600px"
      @close="closeEditDialog"
    >
      <el-form :model="currentEmployee" label-width="160px">
        <el-form-item label="ФИО">
          <el-input v-model="currentEmployee.full_name" />
        </el-form-item>
        <el-form-item label="Должность">
          <el-input v-model="currentEmployee.position" />
        </el-form-item>
        <el-form-item label="Подразделение">
          <el-select v-model="currentEmployee.division" placeholder="Выберите подразделение">
            <el-option 
              v-for="division in divisions" 
              :key="division.id" 
              :label="division.name" 
              :value="division.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Дата рождения">
          <el-date-picker
            v-model="currentEmployee.birth_date"
            type="date"
            placeholder="Выберите дату"
            format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="Дата начала работы">
          <el-date-picker
            v-model="currentEmployee.start_date"
            type="date"
            placeholder="Выберите дату"
            format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="Фото">
          <input type="file" @change="handleEditPhotoUpload" />
          <img 
            v-if="currentEmployee.photo" 
            :src="getPhoto(currentEmployee.photo)" 
            alt="Фото сотрудника" 
            class="preview-photo" 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="closeEditDialog">Отмена</el-button>
        <el-button type="primary" @click="updateEmployee">Сохранить</el-button>
      </template>
    </el-dialog>

    <!-- Модальное окно подтверждения удаления -->
    <el-dialog
      :model-value="showDeleteDialog"
      title="Подтвердить удаление"
      width="400px"
      @close="closeDeleteDialog"
    >
      <span>Вы уверены, что хотите удалить этого сотрудника?</span>
      <template #footer>
        <el-button @click="closeDeleteDialog">Отмена</el-button>
        <el-button type="primary" @click="deleteEmployee">Удалить</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import './Employee.css';
// Преобразование объекта даты в строку формата YYYY-MM-DD
const formatDate = (date) => {
  const d = new Date(date);
  let month = '' + (d.getMonth() + 1);
  let day = '' + d.getDate();
  const year = d.getFullYear();

  if (month.length < 2) month = '0' + month;
  if (day.length < 2) day = '0' + day;

  return [year, month, day].join('-');
};

export default {
  name: 'EmployeeList',
  props: {
    divisionId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      employees: [], // Для хранения сотрудников
      divisions: [],
      showDeleteDialog: false, // Состояние модального окна
      showCreateDialog: false, // Управление модальным окном создания
      showEditDialog: false, // Управление модальным окном редактирования
      employeeToDeleteId: null,
      newEmployee: {
        full_name: '',
        position: '',
        birth_date: '',
        start_date: '',
        photo: '',
        division: this.divisionId, // Автоматическое присвоение divisionId
      },
      currentEmployee: {
        id: null,
        full_name: '',
        position: '',
        birth_date: '',
        start_date: '',
        photo: '',
        division: this.divisionId,
      }, 
    };
  },
  watch: {
    divisionId(newVal) {
      this.newEmployee.division = newVal; // Обновление divisionId при смене выбранного подразделения
    }
  },
  computed: {
    // Фильтр сотрудников по выбранному подразделению
    filteredEmployees() {
      return this.employees.filter(employee => employee.division === this.divisionId);
    },
    employeeCount() {
      return this.filteredEmployees.length;
    },
    averageAge() {
      if (this.employeeCount === 0) return 0;
      const totalAge = this.filteredEmployees.reduce((sum, employee) => {
        const birthDate = new Date(employee.birth_date);
        return sum + (new Date().getFullYear() - birthDate.getFullYear());
      }, 0);
      return Math.floor(totalAge / this.employeeCount);
    },
    averageExperience() {
      if (this.employeeCount === 0) return 0;
      const totalExperience = this.filteredEmployees.reduce((sum, employee) => {
        const startDate = new Date(employee.start_date);
        return sum + (new Date().getFullYear() - startDate.getFullYear());
      }, 0);
      return Math.floor(totalExperience / this.employeeCount);
    }
  },
  methods: {
    formatDate(date) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(date).toLocaleDateString('ru-RU', options);
    },
    // Получение фото из внешнего URL
    getPhoto(photoPath) {
      // Полный путь к фото на сервере
      return `${photoPath}`;
    },
    async fetchDivisions() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/divisions/');
        this.divisions = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке подразделений:', error);
      }
    },
    // Метод для получения сотрудников с сервера
    async fetchEmployees() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/employees/');
        this.employees = response.data; 
      } catch (error) {
        console.error('Ошибка при получении данных сотрудников:', error);
      }
    },
    // Открытие модального окна редактирования
    openEditDialog(employee) {
      this.currentEmployee = { ...employee }; 
      this.showEditDialog = true;
    },
    closeEditDialog() {
      this.showEditDialog = false;
      this.resetCurrentEmployee();
    },
    resetCurrentEmployee() {
      this.currentEmployee = {
        id: null,
        full_name: '',
        position: '',
        birth_date: '',
        start_date: '',
        photo: '',
      };
    },
    // Обработка загрузки нового фото для редактирования
    handleEditPhotoUpload(event) {
      this.currentEmployee.photo = event.target.files[0]; 
    },
    // Обновление сотрудника
    async updateEmployee() {
      try {
        const formData = new FormData();
        formData.append('full_name', this.currentEmployee.full_name);
        formData.append('position', this.currentEmployee.position);
        formData.append('birth_date', formatDate(this.currentEmployee.birth_date));
        formData.append('start_date', formatDate(this.currentEmployee.start_date));
        formData.append('division', this.currentEmployee.division);
        
        if (this.currentEmployee.photo instanceof File) {
          formData.append('photo', this.currentEmployee.photo);
        }

        await axios.patch(`http://127.0.0.1:8000/api/employees/${this.currentEmployee.id}/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });

        this.fetchEmployees();
        this.closeEditDialog();
      } catch (error) {
        console.error('Ошибка при обновлении сотрудника:', error.response.data);
      }
    },
    openCreateDivisionModal() {
      this.showCreateDialog = true; 
    },
    closeCreateDialog() {
      this.showCreateDialog = false; 
      this.resetNewEmployee(); 
    },
    resetNewEmployee() {
      this.newEmployee = {
        full_name: '',
        position: '',
        birth_date: '',
        start_date: '',
        photo: '',
        division: this.divisionId, 
      };
    },
    // Обработка выбора файла
    handlePhotoUpload(event) {
      this.newEmployee.photo = event.target.files[0]; // photo становиться объектом File
    },
    // Загрузка файла на сервер
    async uploadPhoto(file) {
      try {
        const formData = new FormData();
        formData.append('photo', file); // Формируется тело запроса с файлом
        const response = await axios.post('http://127.0.0.1:8000/api/upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        this.newEmployee.photo = response.data.url; // Сохранение URL загруженного фото
      } catch (error) {
        console.error('Ошибка при загрузке фото:', error);
      }
    },
    async createEmployee() {
        const formData = new FormData();
        formData.append('full_name', this.newEmployee.full_name);
        formData.append('position', this.newEmployee.position);
        formData.append('birth_date', formatDate(this.newEmployee.birth_date));
        formData.append('start_date', formatDate(this.newEmployee.start_date));
        formData.append('division', this.newEmployee.division);
        formData.append('photo', this.newEmployee.photo); 
        try {
        await axios.post('http://127.0.0.1:8000/api/employees/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data', 
          },
        });

        this.fetchEmployees();
        this.closeCreateDialog();
      } catch (error) {
        console.error('Ошибка при добавлении сотрудника:', error.response.data);
      }
    },
    openDeleteDialog(employeeId) {
      this.employeeToDeleteId = employeeId; 
      this.showDeleteDialog = true; 
    },
    closeDeleteDialog() {
      this.showDeleteDialog = false; 
      this.employeeToDeleteId = null; 
    },
    // Метод для удаления сотрудника
    async deleteEmployee() {
      try {
        await axios.delete(`http://127.0.0.1:8000/api/employees/${this.employeeToDeleteId}/`);
        this.employees = this.employees.filter(employee => employee.id !== this.employeeToDeleteId);
        this.closeDeleteDialog();
      } catch (error) {
        console.error('Ошибка при удалении сотрудника:', error);
      }
    }
  },
  mounted() {
    this.fetchEmployees(); 
    this.fetchDivisions();
  }
};
</script>
