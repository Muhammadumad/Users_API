# Quick Reference - cURL Commands

Use these commands in PowerShell to test your API directly from terminal.

## Navigation

Open PowerShell and navigate to your project:

```powershell
cd C:\Users\Muhammad Umad\users_api
```

---

## Task 1: Register User

```powershell
$body = @{
    name = "John Doe"
    email = "john@example.com"
    age = 28
    password = "securepassword123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/register/" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

**Save the access_token from response. You'll need it for other requests.**

---

## Task 2: Login User

```powershell
$body = @{
    email = "john@example.com"
    password = "securepassword123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/login/" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

---

## Task 3: Get All Users

Replace `YOUR_ACCESS_TOKEN` with token from Task 1 or 2:

```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_ACCESS_TOKEN"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/users/" `
  -Method GET `
  -Headers $headers
```

---

## Task 4: Get User Details

Replace `USER_ID` with actual UUID from Task 1:

```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_ACCESS_TOKEN"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/users/USER_ID/" `
  -Method GET `
  -Headers $headers
```

---

## Task 5: Update User Profile

```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_ACCESS_TOKEN"
}

$body = @{
    name = "John Updated"
    age = 29
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/users/USER_ID/" `
  -Method PUT `
  -ContentType "application/json" `
  -Headers $headers `
  -Body $body
```

---

## Task 6: Upload Avatar

```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_ACCESS_TOKEN"
}

$filePath = "C:\path\to\your\image.jpg"

$form = @{
    avatar = Get-Item -Path $filePath
}

Invoke-RestMethod -Uri "http://localhost:8000/api/users/avatar/upload/" `
  -Method POST `
  -Headers $headers `
  -Form $form
```

---

## Task 7: Create Blog Post

```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_ACCESS_TOKEN"
}

$body = @{
    title = "My First Blog Post"
    content = "This is an exciting story about Django REST Framework"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/posts/create/" `
  -Method POST `
  -ContentType "application/json" `
  -Headers $headers `
  -Body $body
```

**Save the post id from response**

---

## Task 8: Get All Posts (No Auth Required)

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/posts/" `
  -Method GET
```

---

## Task 9: Get Specific Post

Replace `POST_ID` with actual number:

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/posts/POST_ID/" `
  -Method GET
```

---

## Task 10: Update Your Post

```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_ACCESS_TOKEN"
}

$body = @{
    title = "My First Blog Post – UPDATED"
    content = "Updated content"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/posts/POST_ID/" `
  -Method PUT `
  -ContentType "application/json" `
  -Headers $headers `
  -Body $body
```

---

## Task 11: Add Comment

```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_ACCESS_TOKEN"
}

$body = @{
    content = "Great post! Very informative."
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/posts/POST_ID/comments/" `
  -Method POST `
  -ContentType "application/json" `
  -Headers $headers `
  -Body $body
```

**Save the comment id from response**

---

## Task 12: Get All Comments

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/posts/POST_ID/comments/" `
  -Method GET
```

---

## Task 13: Delete Comment

```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_ACCESS_TOKEN"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/comments/COMMENT_ID/" `
  -Method DELETE `
  -Headers $headers
```

---

## Task 14: Delete Post

```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_ACCESS_TOKEN"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/posts/POST_ID/" `
  -Method DELETE `
  -Headers $headers
```

---

## Task 15: Delete User

```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_ACCESS_TOKEN"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/users/USER_ID/" `
  -Method DELETE `
  -Headers $headers
```

---

## Shortcut Script - Run All Tasks

Save this as `test-all.ps1`:

```powershell
# Configuration
$baseUrl = "http://localhost:8000"
$email = "john@example.com"
$password = "securepassword123"

# Task 1: Register
Write-Host "=== Task 1: Register ===" -ForegroundColor Green
$registerBody = @{
    name = "John Doe"
    email = $email
    age = 28
    password = $password
} | ConvertTo-Json

$registerResponse = Invoke-RestMethod -Uri "$baseUrl/api/register/" `
  -Method POST `
  -ContentType "application/json" `
  -Body $registerBody

$accessToken = $registerResponse.access_token
$userId = $registerResponse.user.id

Write-Host "Access Token: $accessToken"
Write-Host "User ID: $userId"
Write-Host ""

# Task 3: Get All Users
Write-Host "=== Task 3: Get All Users ===" -ForegroundColor Green
$headers = @{ "Authorization" = "Bearer $accessToken" }

$users = Invoke-RestMethod -Uri "$baseUrl/api/users/" `
  -Method GET `
  -Headers $headers

$users | ConvertTo-Json
Write-Host ""

# Task 7: Create Post
Write-Host "=== Task 7: Create Post ===" -ForegroundColor Green
$postBody = @{
    title = "My First Blog Post"
    content = "This is an exciting story"
} | ConvertTo-Json

$postResponse = Invoke-RestMethod -Uri "$baseUrl/api/posts/create/" `
  -Method POST `
  -ContentType "application/json" `
  -Headers $headers `
  -Body $postBody

$postId = $postResponse.id
Write-Host "Post ID: $postId"
Write-Host ""

# Task 8: Get All Posts
Write-Host "=== Task 8: Get All Posts ===" -ForegroundColor Green
$posts = Invoke-RestMethod -Uri "$baseUrl/api/posts/" `
  -Method GET

$posts | ConvertTo-Json
Write-Host ""

# Task 11: Add Comment
Write-Host "=== Task 11: Add Comment ===" -ForegroundColor Green
$commentBody = @{
    content = "Great post!"
} | ConvertTo-Json

$commentResponse = Invoke-RestMethod -Uri "$baseUrl/api/posts/$postId/comments/" `
  -Method POST `
  -ContentType "application/json" `
  -Headers $headers `
  -Body $commentBody

$commentId = $commentResponse.id
Write-Host "Comment ID: $commentId"
Write-Host ""

Write-Host "=== All Tests Completed ===" -ForegroundColor Green
Write-Host "User ID: $userId"
Write-Host "Post ID: $postId"
Write-Host "Comment ID: $commentId"
```

**Run it:**
```powershell
./test-all.ps1
```

---

## Useful Aliases

Add these to your PowerShell profile for faster testing:

```powershell
# Save to PowerShell profile: $PROFILE
$api = "http://localhost:8000"

function Get-ApiToken {
    param(
        [string]$email,
        [string]$password
    )
    
    $body = @{
        email = $email
        password = $password
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$api/api/login/" `
      -Method POST `
      -ContentType "application/json" `
      -Body $body
    
    $response.access_token
}

function Get-ApiUsers {
    param([string]$token)
    
    $headers = @{ "Authorization" = "Bearer $token" }
    Invoke-RestMethod -Uri "$api/api/users/" `
      -Method GET `
      -Headers $headers
}

function Get-ApiPosts {
    Invoke-RestMethod -Uri "$api/api/posts/" -Method GET
}
```

**Then use:**
```powershell
$token = Get-ApiToken "john@example.com" "securepassword123"
Get-ApiUsers $token
Get-ApiPosts
```

