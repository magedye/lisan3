$revisedPath = "d:\APP\tafseer\lisanapp3\main skills\SKILL_LISAN_QURANIC_SEMANTIC_EXTRACTION_REVISED.md"
$execPath = "d:\APP\tafseer\lisanapp3\main skills\Lisan Quranic Semantic Extraction — Executive Protocol.md"
$outPath = "d:\APP\tafseer\lisanapp3\skills\lisan-semantic-extraction\SKILL.md"

$revisedContent = [System.IO.File]::ReadAllText($revisedPath)
$execContent = [System.IO.File]::ReadAllText($execPath)

$startPatterns = $execContent.IndexOf("## 12. Prohibited Patterns")
$endPatterns = $execContent.IndexOf("## 13. Reference Architecture", $startPatterns)
$patternsSection = $execContent.Substring($startPatterns, $endPatterns - $startPatterns)

$startSchema = $execContent.IndexOf("## 11. Presentation Schema")
$endSchema = $execContent.IndexOf("## 12. Prohibited Patterns", $startSchema)
$schemaSection = $execContent.Substring($startSchema, $endSchema - $startSchema)

$finalContent = $revisedContent + "`n`n" + $schemaSection + "`n`n" + $patternsSection
[System.IO.File]::WriteAllText($outPath, $finalContent)
