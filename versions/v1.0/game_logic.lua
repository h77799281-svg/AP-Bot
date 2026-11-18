-- ==========================================
-- AP-ARCHIVE | GAME LOGIC MODULE
-- Мозг системы: коды доступа, токены, статусы
-- ==========================================

local ACCESS_CODES = {
    ["2609"] = { rank = "Admin",   level = "admin" },
    ["2208"] = { rank = "Creator", level = "creator" },
    ["6767"] = { rank = "VIP",     level = "vip_user" }
}

-- Проверка кода доступа
function check_access_code(code)
    local entry = ACCESS_CODES[tostring(code)]
    if entry then
        return entry.rank .. ":" .. entry.level
    end
    return "Denied"
end

-- Генерация уникального токена сессии
function generate_token()
    local chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    local token = ""
    for i = 1, 32 do
        local r = math.random(#chars)
        token = token .. chars:sub(r, r)
    end
    return "AP-" .. token
end

-- Приветствие по роли
function get_greeting(name, level)
    if level == "admin" then
        return "⚡ Администратор " .. name .. " вошёл в систему."
    elseif level == "vip_user" then
        return "👑 Добро пожаловать, " .. name .. "! VIP-статус активирован."
    elseif level == "creator" then
        return "🛠️ Создатель " .. name .. " на связи."
    else
        return "✅ Участник " .. name .. " подключён."
    end
end

-- Цвет бейджа по роли
function get_badge_color(level)
    if level == "admin" then return "#00ff00" end
    if level == "vip_user" then return "#FFD700" end
    if level == "creator" then return "#00FFCC" end
    return "#888888"
end

-- Системные фразы для консоли
function get_system_phrase()
    local phrases = {
        "Антиматерия: стабильна.",
        "Ядро Lua активно.",
        "AP-Net: соединение установлено.",
        "Шифрование токенов: OK.",
        "Система под защитой Лидера."
    }
    return phrases[math.random(#phrases)]
end

-- Валидация ника (только буквы, цифры, _)
function validate_name(name)
    if #name < 2 or #name > 20 then return false end
    if name:match("^[%w_]+$") then return true end
    return false
end

math.randomseed(os.time())
print("[LUA] Модуль game_logic.lua загружен")