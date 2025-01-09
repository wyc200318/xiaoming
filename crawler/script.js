// 初始化成就数组
let achievements = JSON.parse(localStorage.getItem('achievements')) || [];

// 在文件开头添加排序方向变量
let sortDirection = 'desc'; // 默认降序（最新在前）

// 表单提交处理
document.getElementById('achievementForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // 获取表单数据
    const achievement = {
        id: Date.now(),
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        date: document.getElementById('date').value
    };
    
    // 添加到数组并保存
    achievements.push(achievement);
    saveAchievements();
    
    // 重新渲染时间线
    renderTimeline();
    
    // 重置表单
    this.reset();
});

// 保存成就到localStorage
function saveAchievements() {
    localStorage.setItem('achievements', JSON.stringify(achievements));
}

// 添加排序按钮事件监听
document.getElementById('sortDesc').addEventListener('click', function() {
    sortDirection = 'desc';
    updateSortButtonsStyle();
    renderTimeline();
});

document.getElementById('sortAsc').addEventListener('click', function() {
    sortDirection = 'asc';
    updateSortButtonsStyle();
    renderTimeline();
});

// 更新排序按钮样式
function updateSortButtonsStyle() {
    const sortDescBtn = document.getElementById('sortDesc');
    const sortAscBtn = document.getElementById('sortAsc');
    
    // 重置所有按钮样式
    sortDescBtn.className = 'px-4 py-2 rounded-lg transition duration-200 flex items-center space-x-2';
    sortAscBtn.className = 'px-4 py-2 rounded-lg transition duration-200 flex items-center space-x-2';
    
    // 设置激活按钮样式
    if (sortDirection === 'desc') {
        sortDescBtn.className += ' bg-blue-500 text-white hover:bg-blue-600';
        sortAscBtn.className += ' bg-gray-200 hover:bg-gray-300';
    } else {
        sortAscBtn.className += ' bg-blue-500 text-white hover:bg-blue-600';
        sortDescBtn.className += ' bg-gray-200 hover:bg-gray-300';
    }
}

// 修改渲染时间线函数
function renderTimeline() {
    const timeline = document.getElementById('timeline');
    timeline.innerHTML = '';
    
    // 根据排序方向排序
    achievements.sort((a, b) => {
        const dateA = new Date(a.date);
        const dateB = new Date(b.date);
        return sortDirection === 'desc' ? dateB - dateA : dateA - dateB;
    });
    
    // 如果没有成就记录，显示提示信息
    if (achievements.length === 0) {
        timeline.innerHTML = `
            <div class="text-center text-gray-500 py-8">
                还没有记录任何成就，开始添加你的第一个成就吧！
            </div>
        `;
        return;
    }

    // 渲染成就卡片
    achievements.forEach(achievement => {
        const achievementElement = document.createElement('div');
        achievementElement.className = 'bg-white rounded-lg shadow-md p-6 relative achievement-card';
        
        const formattedDate = new Date(achievement.date).toLocaleDateString('zh-CN');
        
        achievementElement.innerHTML = `
            <div class="flex justify-between items-start">
                <div>
                    <h3 class="text-xl font-semibold text-gray-800">${achievement.title}</h3>
                    <p class="text-gray-600 mt-2">${achievement.description}</p>
                </div>
                <div class="flex items-center">
                    <span class="text-gray-500">${formattedDate}</span>
                    <button onclick='openEditModal(${JSON.stringify(achievement).replace(/'/g, "&apos;")})' 
                        class="ml-4 text-blue-500 hover:text-blue-700 transition duration-200">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                        </svg>
                    </button>
                    <button onclick="deleteAchievement(${achievement.id})" 
                        class="ml-4 text-red-500 hover:text-red-700 transition duration-200">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                        </svg>
                    </button>
                </div>
            </div>
        `;
        
        timeline.appendChild(achievementElement);
    });
}

// 删除成就
function deleteAchievement(id) {
    if (confirm('确定要删除这个成就吗？')) {
        achievements = achievements.filter(achievement => achievement.id !== id);
        saveAchievements();
        renderTimeline();
    }
}

// 打开编辑模态框
function openEditModal(achievement) {
    const modal = document.getElementById('editModal');
    const editId = document.getElementById('editId');
    const editTitle = document.getElementById('editTitle');
    const editDescription = document.getElementById('editDescription');
    const editDate = document.getElementById('editDate');
    
    // 填充表单数据
    editId.value = achievement.id;
    editTitle.value = achievement.title;
    editDescription.value = achievement.description;
    editDate.value = achievement.date;
    
    // 显示模态框
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

// 关闭编辑模态框
function closeEditModal() {
    const modal = document.getElementById('editModal');
    modal.classList.remove('flex');
    modal.classList.add('hidden');
}

// 添加编辑表单提交处理
document.getElementById('editForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const id = parseInt(document.getElementById('editId').value);
    const achievement = {
        id: id,
        title: document.getElementById('editTitle').value,
        description: document.getElementById('editDescription').value,
        date: document.getElementById('editDate').value
    };
    
    // 更新成就数组
    const index = achievements.findIndex(item => item.id === id);
    if (index !== -1) {
        achievements[index] = achievement;
        saveAchievements();
        renderTimeline();
        closeEditModal();
    }
});

// 添加点击模态框外部关闭功能
document.getElementById('editModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeEditModal();
    }
});

// 初始渲染
renderTimeline();

// 在初始化时设置默认排序按钮样式
updateSortButtonsStyle(); 