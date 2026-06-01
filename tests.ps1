# Фикс кодировки на уровне процесса
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'
chcp 65001 > $null

$Root = $PSScriptRoot
if (-not $Root) { $Root = Get-Location }
$Total = 0; $Passed = 0; $Failed = 0

function Invoke-Practice {
    param(
        [string]$RelPath,
        [string]$Cmd,
        [hashtable]$EnvVars = $null,
        [string]$PreInstall = $null
    )

    $Global:Total++
    $FullPath = Join-Path $Root $RelPath

    Write-Host "`n============================================================" -ForegroundColor Cyan
    Write-Host "📂 [$Global:Total] $RelPath" -ForegroundColor White
    Write-Host "============================================================" -ForegroundColor Cyan

    if (-not (Test-Path $FullPath)) {
        Write-Host "❌ Папка не найдена: $FullPath" -ForegroundColor Red
        $Global:Failed++
        return
    }

    Push-Location $FullPath
    try {
        # Сброс переменных окружения
        $env:PYTHONPATH = $null
        $env:RUN_SLOW = $null

        # Установка нужных переменных
        if ($EnvVars) {
            foreach ($k in $EnvVars.Keys) { Set-Item -Path "env:$k" -Value $EnvVars[$k] }
        }

        # Предварительная установка зависимостей
        if ($PreInstall) {
            Write-Host "📦 $PreInstall" -ForegroundColor Yellow
            & python -m pip install -q $PreInstall.Split(' ') 2>&1 | Out-Null
        }

        # Запуск тестов
        Write-Host "🏃 $Cmd" -ForegroundColor Green
        # Безопасный вызов без Invoke-Expression
        $ArgsList = $Cmd -split ' '
        & $ArgsList[0] $ArgsList[1..($ArgsList.Length-1)]

        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ УСПЕХ" -ForegroundColor Green
            $Global:Passed++
        } else {
            Write-Host "❌ ОШИБКА (exit code: $LASTEXITCODE)" -ForegroundColor Red
            $Global:Failed++
        }
    } finally {
        Pop-Location
    }
}

# === ЗАПУСК ПРАКТИК ===
Invoke-Practice '01 Модуль 1. База- что и зачем тестируем\1.5 Практика- «скелет» репозитория + минимальный тест по циклу «красный -- зелёный»\qa-unittest-homework' 'python -m unittest discover -s tests -t . -v' @{PYTHONPATH='src'}
Invoke-Practice '02 Модуль 2. TestCase- читаемые и надёжные проверки\2.5 Практика- ветвления и крайние случаи (границы, пустые значения, неверные типы), самодокументируемые тесты\qa-branches-homework' 'python -m unittest discover -s tests -t . -v' @{PYTHONPATH='src'}
Invoke-Practice '03 Модуль 3. Запуск тестов- CLI, точки входа, фильтрация\3.5 Практика- настройка discovery под проект и запуск подмножеств тестов\discovery-lab' 'python -m unittest discover -s tests/unit -t . -p "*_spec.py" -v' @{PYTHONPATH='src'}
Invoke-Practice '03 Модуль 3. Запуск тестов- CLI, точки входа, фильтрация\3.5 Практика- настройка discovery под проект и запуск подмножеств тестов\discovery-lab' 'python -m unittest discover -s tests/integration -t . -p "*_it.py" -v' @{PYTHONPATH='src'}
Invoke-Practice '04 Модуль 4. Fixtures и жизненный цикл теста- setUp-tearDown и cleanup\4.5 Практика- ресурсы (временные файлы-подключения) и доказательство корректной очистки при success-fail-error\cleanup-proof' 'python -m unittest -v'
Invoke-Practice '06 Модуль 6. Управление прогоном- skip, expectedFailure, subTest\6.5 Практика- табличные тесты валидации-парсинга + условные skip по окружению\config-parsing' 'python -m unittest -v' @{RUN_SLOW='1'} 'PyYAML'
Invoke-Practice '07 Модуль 7. Test doubles и unittest.mock- базовые приёмы мокирования\7.5 Практика- подмена внешнего клиента-репозитория мок-объектом и изолированное тестирование бизнес-логики\invoice-service' 'python -m unittest -v'
Invoke-Practice '08 Модуль 8. patch-- правильная подмена зависимостей\8.6 Практика- тест «функция читает ENV -- выбирает поведение» без реальных переменных окружения\payment-router' 'python -m unittest -v'
Invoke-Practice '09 Модуль 9. Спеки, autospec и защита от ложных тестов\9.5 Практика- переход с «голых» моков на autospec и анализ вскрывшихся ошибок\autospec-order-service' 'python -m unittest -v'
Invoke-Practice '10 Модуль 10. Мокирование типовых границ- файлы, классы, сеть, время\10.5 Практика- мини-проект «конфиг -- API-запрос -- обработка ответа» без реального I-O\catalog-snapshot' 'python -m unittest discover -v'
Invoke-Practice '11 Модуль 11. Продвинутые проверки и диагностика- warnings, logs, вывод, скорость\11.5 Практика- «упавший набор -- локализация причины -- исправление -- ускорение медленных тестов»\user-profile-diagnostics' 'python -m unittest discover -v'
Invoke-Practice '12 Модуль 12. Async в unittest- IsolatedAsyncioTestCase и AsyncMock\12.5 Практика- тестирование async-клиента (мок транспортного слоя, retry-timeout сценарии)\async-user-client' 'python -m unittest discover -v'

# === ИТОГИ ===
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "📊 ИТОГО: $Total запусков" -ForegroundColor White
if ($Failed -gt 0) {
    Write-Host "✅ Успешно: $Passed" -ForegroundColor Green
    Write-Host "❌ С ошибками: $Failed" -ForegroundColor Red
} else {
    Write-Host "🎉 ВСЕ ПРАКТИКИ ПРОШЛИ УСПЕШНО!" -ForegroundColor Green
}
Write-Host "============================================================" -ForegroundColor Cyan

if ($Failed -gt 0) { exit 1 } else { exit 0 }