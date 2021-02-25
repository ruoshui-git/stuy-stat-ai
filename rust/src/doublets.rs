use std::{
    collections::HashMap,
    ops::Deref,
};

#[derive(Debug, Default)]
pub struct WordGraph<'a>(HashMap<&'a str, Vec<&'a str>>);

impl<'a> WordGraph<'a> {
    pub fn from_list(words: &'a [String]) -> Self {
        let mut map: HashMap<&str, Vec<&str>> = HashMap::new();

        for word in words.iter() {
            // get all neighbors
            for other in words.iter() {
                if is_neighbor(word, other) {
                    (*map.entry(word).or_insert(vec![])).push(&other);
                }
            }
        }

        Self(map)
    }

    // Hueristic for A*, aka h(x). This currently doesn't depend on the wordlist itself.
    pub fn estimate_distance(&self, src: &str, target: &str) -> usize {
        let mut sum = 0;
        for (a, b) in src.chars().zip(target.chars()) {
            if a != b {
                sum += 1
            }
        }
        return sum;
    }
}

impl<'a> Deref for WordGraph<'a> {
    type Target = HashMap<&'a str, Vec<&'a str>>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct State {
    /// words already in the path
    pub words: Vec<String>,
    /// num words in estimated distance (hueristic)
    pub h: usize,
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        // reverse ordering to make this a min-heap
        // this is g + h
        (other.words.len() + other.h)
            .cmp(&(self.words.len() + self.h))
            // just to stay consistent with PartialEq
            .then_with(|| self.words.cmp(&other.words))
    }
}

impl State {
    pub fn curr(&self) -> &str {
        self.words.last().unwrap()
    }
    // pub fn get_path(&self) -> &Vec<&str> {
    //     &self.words
    // }
}

// impl<'a> State<'a> {
//     fn push(&mut self, word: &'a str) {
//         self.words.push(word)
//     }
//     fn with_next(&self, word: &'a str) -> Self {
//         let mut next_state = self.clone();
//         next_state.push(word);
//         next_state
//     }
// }

fn is_neighbor(a: &str, b: &str) -> bool {
    if a.len() != b.len() || a == b {
        return false;
    }

    let mut has_diff = false;
    for (a, b) in a.chars().zip(b.chars()) {
        if a != b {
            // already has a unmatched character, so they aren't neighbors
            if has_diff {
                return false;
            } else {
                has_diff = true;
            }
        }
    }
    return true;
}

#[cfg(test)]
mod tests {

    use super::*;

    #[test]
    fn test_neighbor_diff_len() {
        assert!(!is_neighbor("abd", "abcd"));
        assert!(!is_neighbor("abc", "abcedf"));
    }

    #[test]
    fn test_neighbor_correct() {
        let cases = [
            ("abcd", "bbcd"),
            ("abcd", "aacd"),
            ("abcd", "abed"),
            ("abcd", "abcc"),
            ("abcde", "fbcde"),
            ("abcdefg", "abcdefh"),
        ];

        for (a, b) in cases.iter() {
            assert!(is_neighbor(a, b))
        }
    }

    #[test]
    fn test_neighbor_too_many_diff() {
        let cases = [
            ("abcd", "abbb", "too many chars different"),
            ("abcd", "abcd", "same words are not neighbors"),
            ("abcde", "bcsdf", "too many chars different"),
        ];

        for (a, b, msg) in cases.iter() {
            assert!(!is_neighbor(a, b), "{}", msg);
        }
    }

    #[test]
    fn test_est_distance() {
        let g = WordGraph::default();
        assert_eq!(3, g.estimate_distance("abc", "def"));
        assert_eq!(1, g.estimate_distance("abcd", "abce"));
        assert_eq!(2, g.estimate_distance("abcd", "abef"));
        assert_eq!(4, g.estimate_distance("abcd", "ecde"));
        assert_eq!(1, g.estimate_distance("abcdefg", "accdefg"));
        assert_eq!(3, g.estimate_distance("sate", "love"));
        assert_eq!(2, g.estimate_distance("late", "love"));
    }
}
