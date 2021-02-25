use std::{
    collections::{BinaryHeap, HashSet},
    env,
    fs::File,
    io::{self, BufRead, BufReader},
};

use stuy_ai::doublets::{State, WordGraph};
fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let src = args
        .get(1)
        .map(String::to_owned)
        .unwrap_or_else(|| "hate".to_string());
    let target = args
        .get(2)
        .map(String::to_owned)
        .unwrap_or_else(|| "love".to_string());

    assert_eq!(src.len(), target.len());
    let len = src.len();

    println!("Loading dict...");

    let words: Vec<String> = BufReader::new(File::open("dictall.txt")?)
        .lines()
        .collect::<io::Result<Vec<String>>>()?
        .into_iter()
        // filter out words with a different size
        .filter(|word| word.len() == len)
        .collect();

    println!("Computing neighbors...");

    let neighbors = WordGraph::from_list(&words);

    let mut frontier = BinaryHeap::new();

    let mut visited = HashSet::new();

    match neighbors.get(src.as_str()) {
        Some(ns) => ns.iter().for_each(|word| {
            frontier.push(State {
                words: vec![word.to_string()],
                h: neighbors.estimate_distance(word, &target),
            });
        }),

        None => {
            panic!("The word you started with isn't in the dictionary. Try another one instead.")
        }
    };

    // eprintln!("first neighbors: {:?}", frontier);

    println!("Finding path...");

    while let Some(node) = frontier.pop() {
        let curr = node.curr();
        if visited.contains(curr) {
            continue;
        } else {
            visited.insert(curr.to_owned());
        }
        // eprintln!("curr path: {:?}", node.words);
        if curr == target.as_str() {
            // println!(
            //     "found path of len {} for {} to {}",
            //     node.words.len(),
            //     src,
            //     target
            // );
            let mut path = vec![src];
            path.extend(node.words);
            let report_str = format!("{:?}", (path.len(), path)).replace("\"", "'");
            println!("{}", report_str);
            return Ok(());
        }

        for word in neighbors
            .get(curr)
            .expect("Error: intermediate word not in dict")
        {
            let mut new_words = node.words.clone();
            new_words.push(word.to_string());

            frontier.push(State {
                words: new_words.clone(),
                h: neighbors.estimate_distance(word, &target),
            });

            // eprintln!("new path: {:?}", new_words)
        }
    }

    println!("No path found");
    Ok(())
}
