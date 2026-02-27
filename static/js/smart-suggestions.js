/**
 * Smart Suggestions for Questionnaire
 * 
 * Loads suggestion rules from backend and evaluates them in real-time
 * for instant feedback to users.
 */

class SmartSuggestions {
    constructor() {
        this.rules = [];
        this.rulesVersion = null;
        this.currentResponses = {};
    }

    /**
     * Initialize by loading rules from backend
     */
    async init() {
        try {
            const response = await fetch('/api/suggestion-rules');
            const data = await response.json();
            this.rules = data.rules;
            this.rulesVersion = data.version;
            this.fieldOrder = data.field_order || {};
            console.log(`Loaded ${this.rules.length} suggestion rules (v${this.rulesVersion}) with structural order`);
        } catch (error) {
            console.error('Failed to load suggestion rules:', error);
        }
    }

    /**
     * Update current responses and re-evaluate
     */
    updateResponses(responses) {
        this.currentResponses = responses;
        return this.evaluateSuggestions();
    }

    /**
     * Check if a condition matches current responses
     */
    _matchesCondition(condition, responses) {
        for (const [field, expectedValue] of Object.entries(condition)) {
            const actualValue = responses[field];

            // Handle array of acceptable values
            if (Array.isArray(expectedValue)) {
                if (!expectedValue.includes(actualValue)) {
                    return false;
                }
            } else {
                if (actualValue !== expectedValue) {
                    return false;
                }
            }
        }
        return true;
    }

    /**
     * Evaluate all rules against current responses
     */
    evaluateSuggestions() {
        const suggestionsByField = {}; // Group by field, keep only highest priority

        // Sort by priority (highest first)
        const sortedRules = [...this.rules].sort((a, b) =>
            (b.priority || 0) - (a.priority || 0)
        );

        for (const rule of sortedRules) {
            // STRUCTURAL PROTECTION: Enforce unidirectional flow
            const targetField = rule.suggestion.field;
            // Default to 99 (end of form) if not found to be safe
            const targetOrder = this.fieldOrder[targetField] ?? 99;

            let isRetroactive = false;
            for (const condField of Object.keys(rule.condition)) {
                // Default to 0 (beginning of form) if not found
                const condOrder = this.fieldOrder[condField] ?? 0;

                // CRITICAL: Target MUST be strictly after Condition
                // If target index <= condition index, it's a retroactive/looping rule
                if (targetOrder <= condOrder) {
                    isRetroactive = true;
                    break;
                }
            }

            if (isRetroactive) continue;

            if (this._matchesCondition(rule.condition, this.currentResponses)) {
                const field = rule.suggestion.field;
                const currentValue = this.currentResponses[field];

                // PRIORITY FILTERING: Only keep highest priority suggestion per field
                if (suggestionsByField[field]) {
                    const existingSuggestion = suggestionsByField[field];
                    if ((rule.priority || 0) <= (existingSuggestion.priority || 0)) {
                        // This rule has lower or equal priority, skip it
                        continue;
                    }
                }

                suggestionsByField[field] = {
                    ruleId: rule.id,
                    field: field,
                    suggestedValues: rule.suggestion.suggested_values,
                    explanation: rule.suggestion.explanation,
                    confidence: rule.suggestion.confidence,
                    priority: rule.priority || 0,
                    currentValue: currentValue,
                    isFollowed: currentValue && rule.suggestion.suggested_values.includes(currentValue)
                };
            }
        }

        // Convert to array
        return Object.values(suggestionsByField);
    }

    /**
     * Calculate coherence score
     */
    calculateCoherence() {
        const suggestions = this.evaluateSuggestions();

        if (suggestions.length === 0) {
            return {
                status: 'excellent',
                message: 'Profil très cohérent',
                followedCount: 0,
                totalCount: 0
            };
        }

        const followed = suggestions.filter(s => s.isFollowed).length;
        const total = suggestions.length;
        const ratio = total > 0 ? followed / total : 1.0;

        // Pedagogical scoring (never judgmental)
        let status, message;
        if (ratio >= 0.8) {
            status = 'excellent';
            message = 'Profil très cohérent';
        } else if (ratio >= 0.5) {
            status = 'good';
            message = 'Profil cohérent';
        } else {
            status = 'needs_reflection';
            // NEVER negative language
            message = 'Certaines réponses méritent réflexion';
        }

        return {
            status,
            message,
            followedCount: followed,
            totalCount: total
        };
    }

    /**
     * Get suggestions for a specific field
     */
    getSuggestionsForField(field) {
        const all = this.evaluateSuggestions();
        return all.filter(s => s.field === field);
    }
}

// Singleton instance
const smartSuggestions = new SmartSuggestions();
